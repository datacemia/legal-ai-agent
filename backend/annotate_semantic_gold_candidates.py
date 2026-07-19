#!/usr/bin/env python3
"""Build a human-review GOLD CANDIDATE pack from review_pack_60.jsonl.

This is NOT a gold-label generator and never marks rows APPROVED.

Design:
- source-text only candidate annotation;
- multilingual canonical concepts (EN/FR/AR);
- exact source evidence spans with offset verification;
- candidate primary type derived from candidate domain mechanisms only;
- all rows remain REVIEW_REQUIRED;
- no contract-agent imports;
- no publication-gate or pipeline mutation.

Outputs:
- review_pack_60_gold_candidate.jsonl
- review_pack_60_gold_candidate.csv
- review_pack_60_gold_candidate_summary.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")


@dataclass(frozen=True)
class Rule:
    mechanism: str
    primary_type: str | None
    role: str
    patterns: dict[str, tuple[str, ...]]
    polarity: str | None = None
    procedural_state: str | None = None
    numeric_role: str | None = None
    priority: int = 50


RULES: tuple[Rule, ...] = (
    Rule(
        "TERMINATION_RIGHT",
        "termination",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bmay terminate\b.{0,220}",
                r"\bterminate only for\b.{0,220}",
            ),
            "fr": (
                r"\bpourra résilier\b.{0,220}",
                r"\bne pourra résilier que\b.{0,220}",
                r"\bpeut résilier\b.{0,220}",
            ),
            "ar": (
                r"(?:يجوز|يحق).{0,40}(?:الإنهاء|إنهاء).{0,220}",
            ),
        },
        polarity="RIGHT",
        priority=100,
    ),
    Rule(
        "TERMINATION_FOR_CAUSE",
        "termination",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\b(?:material|uncured material) breach\b.{0,180}",
            ),
            "fr": (
                r"\bmanquement substantiel\b.{0,180}",
            ),
            "ar": (
                r"(?:إخلال|خرق).{0,40}(?:جوهري|جسيم).{0,180}",
            ),
        },
        procedural_state="CAUSE_TRIGGER",
        priority=98,
    ),
    Rule(
        "CURE_PERIOD",
        "termination",
        "PROCEDURAL_STATE",
        {
            "en": (
                r"\b(?:sixty|thirty|forty[- ]five|seventy[- ]two|forty[- ]eight)\s*\(\d+\)\s+days?['’]?\s+written notice and opportunity to cure\b",
                r"\bopportunity to cure\b",
            ),
            "fr": (
                r"\bpossibilité de remédier\b",
                r"\bdélai de .{0,30}jours.{0,80}remédier\b",
            ),
            "ar": (
                r"(?:مهلة|فرصة).{0,50}(?:للمعالجة|لتصحيح|لإصلاح)",
                r"غير معالج.{0,120}إشعار",
            ),
        },
        procedural_state="CURE_REQUIRED",
        priority=96,
    ),
    Rule(
        "NOTICE_REQUIREMENT",
        None,
        "CONTROL_MODIFIER",
        {
            "en": (
                r"\bupon written notice\b",
                r"\bwritten notice\b",
                r"\bwithin .{0,40} hours\b",
                r"\bwithout undue delay\b",
            ),
            "fr": (
                r"\bmoyennant notification écrite\b",
                r"\bpréavis écrit\b",
                r"\bdans un délai de .{0,40}heures\b",
                r"\bsans délai injustifié\b",
            ),
            "ar": (
                r"(?:إشعار|إخطار) خطي",
                r"(?:خلال|في غضون).{0,40}(?:ساعة|ساعات)",
            ),
        },
        procedural_state="NOTICE_REQUIRED",
        priority=95,
    ),
    Rule(
        "FEE_ADJUSTMENT_RIGHT",
        "renewal",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\breserves the right to unilaterally increase fees\b.{0,220}",
            ),
            "fr": (
                r"\bse réserve le droit d['’]augmenter unilatéralement les honoraires\b.{0,220}",
            ),
            "ar": (
                r"يحتفظ.{0,80}بالحق في زيادة الرسوم من جانب واحد.{0,220}",
            ),
        },
        polarity="RIGHT",
        priority=94,
    ),
    Rule(
        "PAYMENT_OBLIGATION",
        "payment",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall pay\b.{0,220}",
                r"\bpayable monthly\b",
            ),
            "fr": (
                r"\bpaiera\b.{0,220}",
                r"\bpayable mensuellement\b",
            ),
            "ar": (
                r"(?:يدفع|تدفع|يُدفع|تُدفع).{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=93,
    ),
    Rule(
        "PAYMENT_DEADLINE",
        "payment",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bwithin [^.]{0,60}\(\d+\)\s+days of the invoice date\b",
            ),
            "fr": (
                r"\bdans un délai de [^.]{0,60}\(\d+\)\s+jours à compter de la date de facturation\b",
            ),
            "ar": (
                r"(?:خلال|في غضون).{0,60}\(\d+\).{0,20}(?:يوماً|يومًا|يوم|أيام).{0,80}(?:الفاتورة|الفوترة)",
            ),
        },
        procedural_state="DEADLINE",
        numeric_role="PAYMENT_DEADLINE_DAYS",
        priority=92,
    ),
    Rule(
        "INTEREST_ACCRUAL",
        "payment",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall accrue interest at\b.{0,120}",
                r"\bshall bear interest at\b.{0,120}",
            ),
            "fr": (
                r"\bportera intérêt au taux de\b.{0,120}",
                r"\bportera intérêt à un taux\b.{0,120}",
            ),
            "ar": (
                r"(?:يحمل|تترتب|يترتب).{0,80}(?:فائدة|فوائد).{0,120}",
            ),
        },
        priority=91,
    ),
    Rule(
        "COST_ALLOCATION",
        "fees",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\beach Party shall bear its own costs and expenses\b.{0,220}",
                r"\bshared costs shall be split equally\b",
            ),
            "fr": (
                r"\bchaque Partie.{0,50}(?:supportera|assumera).{0,120}(?:coûts|frais)\b",
                r"\bcoûts partagés.{0,80}(?:répartis|partagés) à parts égales\b",
            ),
            "ar": (
                r"(?:يتحمل|تتحمل) كل طرف.{0,80}(?:تكاليف|مصاريف)",
                r"(?:التكاليف|المصاريف) المشتركة.{0,80}(?:بالتساوي|مناصفة)",
            ),
        },
        priority=90,
    ),
    Rule(
        "PRICE_ADJUSTMENT_MECHANISM",
        "pricing",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bprices .{0,80}shall remain fixed\b.{0,220}",
                r"\badjustment no more than once annually\b.{0,180}",
                r"\bcapped at \d+(?:\.\d+)?% per year\b",
            ),
            "fr": (
                r"\bprix .{0,80}(?:resteront|demeureront) fixes\b.{0,220}",
                r"\bajustement .{0,120}une fois par an\b",
            ),
            "ar": (
                r"(?:الأسعار|الأسعار).{0,80}(?:ثابتة|تبقى ثابتة).{0,220}",
                r"(?:تعديل|زيادة).{0,120}(?:مرة واحدة سنوياً|مرة سنويًا)",
            ),
        },
        priority=89,
    ),
    Rule(
        "PURCHASE_COMMITMENT",
        "supply_distribution",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall purchase at least\b.{0,220}",
                r"\bbuy at least\b.{0,220}",
            ),
            "fr": (
                r"\bachètera au moins\b.{0,220}",
            ),
            "ar": (
                r"يشتري.{0,80}ما لا يقل عن.{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=88,
    ),
    Rule(
        "INDEMNIFICATION_OBLIGATION",
        "indemnity",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall indemnify\b.{0,260}",
            ),
            "fr": (
                r"\bindemnisera\b.{0,260}",
            ),
            "ar": (
                r"(?:يعوض|تعوض).{0,260}",
            ),
        },
        polarity="REQUIRED",
        priority=87,
    ),
    Rule(
        "LIABILITY_CAP",
        "liability",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\baggregate liability\b.{0,100}\b(?:not exceed|shall not exceed|limited to)\b.{0,180}",
            ),
            "fr": (
                r"\bresponsabilité globale\b.{0,120}\bn['’]excédera pas\b.{0,180}",
            ),
            "ar": (
                r"(?:لا تتجاوز|لا تجاوز).{0,60}المسؤولية الإجمالية.{0,220}",
                r"المسؤولية الإجمالية.{0,120}(?:لا تتجاوز|محددة|محدودة).{0,180}",
            ),
        },
        priority=86,
    ),
    Rule(
        "LIABILITY_CARVEOUT",
        "liability",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bexcept for breaches of confidentiality or indemnification obligations\b",
                r"\bexcept for\b.{0,120}(?:confidentiality|indemnification|gross negligence|willful misconduct)\b",
            ),
            "fr": (
                r"\b(?:sauf|à l['’]exception).{0,160}(?:confidentialité|indemnisation|négligence grave|faute intentionnelle)\b",
                r"\bsera illimitée en cas de négligence grave ou de faute intentionnelle\b",
            ),
            "ar": (
                r"\bباستثناء\b.{0,180}(?:الأمن|التعويض|الإهمال الجسيم|السلوك المتعمد)",
            ),
        },
        procedural_state="CARVEOUT",
        priority=85,
    ),
    Rule(
        "EXCLUDED_DAMAGE_CATEGORY",
        "liability",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\b(?:indirect|consequential|punitive) damages\b.{0,180}",
            ),
            "fr": (
                r"\bdommages\b.{0,80}(?:indirects|consécutifs|punitifs).{0,180}",
            ),
            "ar": (
                r"الأضرار.{0,80}(?:غير المباشرة|التبعية|العقابية).{0,180}",
            ),
        },
        polarity="EXCLUDED",
        priority=84,
    ),
    Rule(
        "BACKGROUND_IP_RETENTION",
        "intellectual_property",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bretains all right, title, and interest in its pre-existing\b.{0,220}",
            ),
            "fr": (
                r"\bconserve la propriété de ses .{0,120}préexistants\b.{0,220}",
            ),
            "ar": (
                r"يحتفظ.{0,80}بكامل الحقوق في.{0,120}السابقة.{0,220}",
            ),
        },
        polarity="RIGHT",
        priority=83,
    ),
    Rule(
        "IP_ASSIGNMENT",
        "intellectual_property",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bassigns? .{0,80}all right, title, and interest\b.{0,220}",
            ),
            "fr": (
                r"\bcède par les présentes\b.{0,240}l['’]intégralité des droits\b",
            ),
            "ar": (
                r"(?:يتنازل|تحيل|يحول).{0,100}(?:جميع الحقوق|كافة الحقوق).{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=82,
    ),
    Rule(
        "WORK_PRODUCT_OWNERSHIP_TRANSFER",
        "work_product",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bdeliverables .{0,120}(?:work made for hire|exclusive property)\b.{0,180}",
                r"\bshall become the exclusive property\b.{0,180}",
            ),
            "fr": (
                r"\btous les Livrables\b.{0,160}\bdeviendront la propriété exclusive\b.{0,180}",
            ),
            "ar": (
                r"(?:جميع المخرجات).{0,120}(?:تؤول ملكيتها حصراً|الملكية الحصرية).{0,180}",
            ),
        },
        procedural_state="OWNERSHIP_TRANSFER",
        priority=81,
    ),
    Rule(
        "LICENSE_RESTRICTION",
        "license",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall not reverse engineer, decompile, or create derivative works\b.{0,220}",
            ),
            "fr": (
                r"\bne .{0,30}(?:procédera|pourra).{0,60}(?:ingénierie inverse|décompiler|œuvres dérivées).{0,220}",
            ),
            "ar": (
                r"(?:لا يجوز|يمتنع).{0,80}(?:الهندسة العكسية|فك التجميع|أعمال مشتقة).{0,220}",
            ),
        },
        polarity="PROHIBITED",
        priority=80,
    ),
    Rule(
        "CONFIDENTIAL_USE_RESTRICTION",
        "confidentiality",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall use the Confidential Information solely for the Purpose\b",
            ),
            "fr": (
                r"\bn['’]utilisera les Informations Confidentielles qu['’]aux fins de l['’]Objet\b",
            ),
            "ar": (
                r"(?:يستخدم|تستخدم).{0,80}(?:المعلومات السرية).{0,80}(?:فقط|حصراً).{0,80}(?:الغرض|الغاية)",
            ),
        },
        polarity="RESTRICTED",
        priority=79,
    ),
    Rule(
        "CONFIDENTIALITY_EXCLUSION",
        "confidentiality",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bconfidential information does not include\b.{0,320}",
            ),
            "fr": (
                r"\bles informations confidentielles ne comprennent pas\b.{0,320}",
                r"\bne sont pas considérées comme informations confidentielles\b.{0,320}",
            ),
            "ar": (
                r"لا تشمل المعلومات السرية المعلومات التي.{0,320}",
            ),
        },
        procedural_state="EXCLUSION",
        priority=78,
    ),
    Rule(
        "DATA_PROCESSING_INSTRUCTION_LIMIT",
        "data_protection",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bprocess personal data only on documented instructions\b.{0,260}",
            ),
            "fr": (
                r"\bne traitera les Données Personnelles que sur instructions documentées\b.{0,260}",
            ),
            "ar": (
                r"(?:لا يعالج|لا تعالج).{0,80}(?:البيانات الشخصية).{0,80}(?:تعليمات|توجيهات).{0,220}",
            ),
        },
        polarity="RESTRICTED",
        priority=77,
    ),
    Rule(
        "DATA_SUBJECT_ASSISTANCE",
        "data_processing",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall assist Controller\b.{0,220}\bdata subject rights\b.{0,180}",
            ),
            "fr": (
                r"\bassistera le Responsable du Traitement\b.{0,220}\bdroits des personnes concernées\b.{0,180}",
            ),
            "ar": (
                r"(?:يساعد|تساعد).{0,100}(?:مسؤول المعالجة|المتحكم).{0,220}(?:حقوق أصحاب البيانات|حقوق الأشخاص المعنيين)",
            ),
        },
        polarity="REQUIRED",
        priority=76,
    ),
    Rule(
        "BREACH_NOTIFICATION",
        "data_protection",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall notify Controller\b.{0,180}\bPersonal Data breach\b.{0,220}",
                r"\bnotify Customer of any confirmed security incident\b.{0,220}",
            ),
            "fr": (
                r"\bnotifiera .{0,120}(?:incident de sécurité|violation de données)\b.{0,220}",
            ),
            "ar": (
                r"(?:يخطر|تخطر).{0,100}(?:حادث أمني|خرق بيانات|انتهاك بيانات).{0,220}",
            ),
        },
        polarity="REQUIRED",
        procedural_state="NOTIFICATION",
        priority=75,
    ),
    Rule(
        "SECURITY_SAFEGUARD_OBLIGATION",
        "security",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall maintain administrative, physical, and technical safeguards\b.{0,220}",
            ),
            "fr": (
                r"\bmaintiendra des mesures de sauvegarde administratives, physiques et techniques\b.{0,220}",
            ),
            "ar": (
                r"(?:يحافظ|تحافظ).{0,80}(?:ضمانات|تدابير).{0,80}(?:إدارية|تقنية|مادية).{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=74,
    ),
    Rule(
        "DATA_EXPORT_WINDOW",
        "data_protection",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bafter termination\b.{0,100}\bavailable for export\b.{0,160}",
            ),
            "fr": (
                r"\baprès la résiliation\b.{0,100}\bexport\b.{0,160}",
            ),
            "ar": (
                r"عند الإنهاء.{0,120}(?:للتصدير|تصدير).{0,160}",
            ),
        },
        procedural_state="POST_TERMINATION_EXPORT",
        priority=73,
    ),
    Rule(
        "DATA_DELETION_RIGHT",
        "data_protection",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bthereafter may be permanently deleted\b",
            ),
            "fr": (
                r"\bpeuvent ensuite être supprimées définitivement\b",
            ),
            "ar": (
                r"بعد ذلك يجوز حذفها نهائياً",
            ),
        },
        polarity="OPTION",
        procedural_state="POST_EXPORT_DELETION",
        priority=72,
    ),
    Rule(
        "LOAN_DISBURSEMENT",
        "loan",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bLender shall disburse the principal amount of the Loan\b.{0,220}",
            ),
            "fr": (
                r"\bLe Prêteur décaissera le montant en principal du Prêt\b.{0,220}",
            ),
            "ar": (
                r"يصرف المُقرض المبلغ الأصلي للقرض.{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=71,
    ),
    Rule(
        "CONDITIONS_PRECEDENT",
        "loan",
        "PROCEDURAL_STATE",
        {
            "en": (
                r"\bupon satisfaction of the conditions precedent\b.{0,160}",
            ),
            "fr": (
                r"\bsous réserve de la satisfaction des conditions préalables\b.{0,160}",
            ),
            "ar": (
                r"رهناً باستيفاء الشروط المسبقة.{0,160}",
            ),
        },
        procedural_state="CONDITION_PRECEDENT",
        priority=70,
    ),
    Rule(
        "SECURITY_INTEREST_GRANT",
        "security_interest",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bgrants Lender a first-priority security interest\b.{0,220}",
            ),
            "fr": (
                r"\bconsent au Prêteur une sûreté de premier rang\b.{0,220}",
            ),
            "ar": (
                r"(?:يمنح|يقدم).{0,80}(?:حق ضمان|مصلحة ضمانية|سند ضمان).{0,220}",
            ),
        },
        polarity="GRANT",
        priority=69,
    ),
    Rule(
        "GUARANTEE_SUPPORT",
        "guarantee",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bobligations .{0,100} are guaranteed by\b.{0,220}",
            ),
            "fr": (
                r"\bobligations .{0,100} sont garanties par\b.{0,220}",
            ),
            "ar": (
                r"التزامات.{0,100}مكفولة من قبل.{0,220}",
            ),
        },
        procedural_state="GUARANTEED",
        priority=68,
    ),
    Rule(
        "EMPLOYMENT_ROLE_DUTY",
        "employment",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bExecutive shall serve as\b.{0,180}",
                r"\bshall devote substantially full business time\b.{0,180}",
            ),
            "fr": (
                r"\bLa Dirigeante exercera les fonctions de\b.{0,180}",
                r"\bconsacrera l['’]essentiel de son temps de travail\b.{0,180}",
            ),
            "ar": (
                r"(?:تعمل|تشغل|تتولى).{0,80}(?:منصب|وظيفة).{0,180}",
                r"(?:تكرس|تخصص).{0,80}(?:وقت العمل|وقتها).{0,180}",
            ),
        },
        polarity="REQUIRED",
        priority=67,
    ),
    Rule(
        "BASE_COMPENSATION",
        "compensation",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bbase salary\b.{0,180}",
            ),
            "fr": (
                r"\bsalaire de base\b.{0,180}",
            ),
            "ar": (
                r"(?:راتباً أساسياً|الراتب الأساسي).{0,180}",
            ),
        },
        priority=66,
    ),
    Rule(
        "NON_COMPETE_RESTRICTION",
        "restrictive_covenants",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall not .{0,80}provide services to any entity that directly competes\b.{0,220}",
            ),
            "fr": (
                r"\bne .{0,40}fournira .{0,80}services à une entité qui concurrence directement\b.{0,220}",
            ),
            "ar": (
                r"تمتنع.{0,100}عن تقديم خدمات لأي جهة تنافس مباشرة.{0,220}",
            ),
        },
        polarity="PROHIBITED",
        priority=65,
    ),
    Rule(
        "NON_SOLICITATION_RESTRICTION",
        "restrictive_covenants",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall not solicit any employee\b.{0,220}",
            ),
            "fr": (
                r"\bne sollicitera aucun salarié\b.{0,220}",
            ),
            "ar": (
                r"تمتنع.{0,80}عن استقطاب أي موظف.{0,220}",
            ),
        },
        polarity="PROHIBITED",
        priority=64,
    ),
    Rule(
        "OPERATIONAL_COVENANT",
        "covenant",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bSeller shall operate the Business in the ordinary course consistent with past practice\b.{0,260}",
            ),
            "fr": (
                r"\bLe Vendeur exploitera l['’]Activité dans le cours normal des affaires\b.{0,260}",
            ),
            "ar": (
                r"(?:يشغل|يدير).{0,80}(?:النشاط|الأعمال).{0,80}(?:المسار العادي|السياق المعتاد).{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=63,
    ),
    Rule(
        "SERVICE_PERFORMANCE_OBLIGATION",
        "services",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bshall perform the services described in each SOW\b.{0,220}",
            ),
            "fr": (
                r"\bexécutera les services décrits dans chaque Bon de Commande\b.{0,220}",
            ),
            "ar": (
                r"(?:ينفذ|يقدم).{0,80}(?:الخدمات).{0,120}(?:أمر العمل|نطاق العمل).{0,180}",
            ),
        },
        polarity="REQUIRED",
        priority=62,
    ),
    Rule(
        "SERVICE_LEVEL_COMMITMENT",
        "service_level",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bmaintain 99\.9% uptime\b.{0,220}",
            ),
            "fr": (
                r"\bmaintenir une disponibilité de 99[,.]9 ?%\b.{0,220}",
            ),
            "ar": (
                r"(?:توافر|إتاحة).{0,80}99[,.]9 ?%.{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=61,
    ),
    Rule(
        "SOLE_EXCLUSIVE_REMEDY",
        "remedies",
        "CONTROL_MODIFIER",
        {
            "en": (
                r"\bsole and exclusive remedy\b.{0,180}",
            ),
            "fr": (
                r"\bseul et unique recours\b.{0,180}",
            ),
            "ar": (
                r"(?:العلاج|الجزاء|الانتصاف).{0,40}(?:الوحيد والحصري|الحصري الوحيد).{0,180}",
            ),
        },
        procedural_state="EXCLUSIVE_REMEDY",
        priority=60,
    ),
    Rule(
        "DELIVERY_OBLIGATION",
        "delivery",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bSupplier shall deliver\b.{0,220}",
            ),
            "fr": (
                r"\bLe Fournisseur livrera\b.{0,220}",
            ),
            "ar": (
                r"يسلم المورد.{0,220}",
            ),
        },
        polarity="REQUIRED",
        priority=59,
    ),
    Rule(
        "PREEMPTIVE_RIGHT",
        "anti_dilution_preemptive_rights",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bright to purchase its pro rata share of any new securities\b.{0,220}",
            ),
            "fr": (
                r"\bdroit d['’]acheter sa quote-part proportionnelle de tout nouveau titre\b.{0,220}",
            ),
            "ar": (
                r"يحق للمستثمر شراء حصته التناسبية من أي أوراق مالية جديدة.{0,220}",
            ),
        },
        polarity="RIGHT",
        priority=58,
    ),
    Rule(
        "TAG_ALONG_RIGHT",
        "share_transfer_rights",
        "DOMAIN_MECHANISM",
        {
            "en": (
                r"\bright to participate in such sale on the same terms\b.{0,220}",
            ),
            "fr": (
                r"\bdroit de participer à cette vente aux mêmes conditions\b.{0,220}",
            ),
            "ar": (
                r"يحق للمستثمر المشاركة في هذا البيع بنفس الشروط.{0,220}",
            ),
        },
        polarity="RIGHT",
        priority=57,
    ),
)


PRIMARY_TYPE_EQUIVALENCE = {
    "automatic_renewal": "renewal",
    "limitation_of_liability": "liability",
    "ownership": "intellectual_property",
    "work_product": "intellectual_property",
}


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise RuntimeError(
                    f"{path}:{line_number}: expected JSON object"
                )
            rows.append(value)
    return rows


def valid_span(source: str, span: dict) -> bool:
    start = span.get("start")
    end = span.get("end")
    text = span.get("text")
    return (
        isinstance(start, int)
        and isinstance(end, int)
        and 0 <= start < end <= len(source)
        and source[start:end] == text
    )


def collect_spans(source: str, pattern: str, mechanism: str) -> list[dict]:
    spans = []
    for match in re.finditer(pattern, source, re.I | re.S):
        span = {
            "mechanism": mechanism,
            "start": match.start(),
            "end": match.end(),
            "text": match.group(0),
        }
        if valid_span(source, span):
            spans.append(span)
    return spans


def numeric_roles(
    source: str,
    language: str,
    mechanisms: list[dict],
) -> list[dict]:
    results = []

    patterns = {
        "en": (
            r"\bwithin ([a-z-]+)\s*\((\d+)\)\s+(hours?|days?)\b",
            r"\bafter ([a-z-]+)\s*\((\d+)\)\s+(days?)\b",
            r"\bfor the first ([a-z-]+)\s*\((\d+)\)\s+(months?|years?)\b",
            r"\bup to ([a-z-]+) percent\s*\((\d+)%\)",
            r"\b(\d+(?:\.\d+)?)%\s+per\s+(month|year|annum)\b",
            r"\b(\d+(?:\.\d+)?)%\s+uptime\b",
        ),
        "fr": (
            r"\bdans un délai de ([a-zàâçéèêëîïôùûüÿœæ-]+)\s*\((\d+)\)\s+(heures?|jours?)\b",
            r"\baprès ([a-zàâçéèêëîïôùûüÿœæ-]+)\s*\((\d+)\)\s+(jours?)\b",
            r"\bjusqu['’]à ([a-zàâçéèêëîïôùûüÿœæ-]+) pour cent\s*\((\d+)\s*%\)",
            r"\b(\d+(?:[,.]\d+)?)\s*%\s+par\s+(mois|an)\b",
            r"\b(\d+(?:[,.]\d+)?)\s*%\s+de disponibilité\b",
        ),
        "ar": (
            r"(?:خلال|لمدة|مدته)\s+([^\s،.؛]+)\s*\((\d+)\)\s+(ساعة|ساعات|يوماً|يومًا|يوم|أيام|شهراً|شهرًا|شهر|سنوات|سنة)",
            r"(\d+(?:\.\d+)?)%\s*(?:سنوياً|سنويًا|شهرياً|شهريًا)",
            r"(\d+(?:\.\d+)?)%\s*(?:من|توافر|إتاحة)",
        ),
    }

    for pattern in patterns.get(language, ()):
        for match in re.finditer(pattern, source, re.I | re.S):
            text = match.group(0)
            role = "NUMERIC_TERM"

            lower = text.lower()

            if any(token in lower for token in (
                "hours", "heure", "ساعة", "ساعات"
            )):
                role = "NOTICE_OR_BREACH_NOTIFICATION_HOURS"
            elif any(token in lower for token in (
                "days", "jours", "يوم", "أيام", "يوماً", "يومًا"
            )):
                role = "DEADLINE_OR_NOTICE_DAYS"
            elif any(token in lower for token in (
                "months", "mois", "شهر", "شهراً", "شهرًا"
            )):
                role = "DURATION_MONTHS"
            elif any(token in lower for token in (
                "years", "year", "an", "سنوات", "سنة"
            )):
                role = "DURATION_YEARS"
            elif "%" in text:
                role = "PERCENTAGE_THRESHOLD_OR_RATE"

            results.append({
                "role": role,
                "start": match.start(),
                "end": match.end(),
                "text": text,
            })

    return results


def extract_actor_object_arguments(
    source: str,
    language: str,
    mechanisms: list[dict],
) -> list[dict]:
    results = []

    for mechanism in mechanisms:
        spans = mechanism.get("source_evidence") or []
        if not spans:
            continue

        evidence = spans[0]
        text = evidence["text"]

        if language == "en":
            actor_match = re.match(
                r"^\s*(?:\d+(?:\.\d+)?\s+)?(.{1,80}?)\s+(?:shall|may|reserves|retains|grants|are guaranteed)\b",
                text,
                re.I | re.S,
            )
        elif language == "fr":
            actor_match = re.match(
                r"^\s*(?:\d+(?:\.\d+)?\s+)?(.{1,80}?)\s+(?:paiera|pourra|indemnisera|conserve|cède|exécutera|décaissera|consent|exercera|maintiendra)\b",
                text,
                re.I | re.S,
            )
        else:
            actor_match = re.match(
                r"^\s*(?:\d+(?:\.\d+)?\s+)?(.{1,80}?)\s+(?:يجوز|يحق|يدفع|تدفع|يعوض|يحتفظ|يصرف|يسلم|تمتنع|يحافظ|تحافظ)\b",
                text,
                re.I | re.S,
            )

        actor = (
            actor_match.group(1).strip()
            if actor_match
            else ""
        )

        results.append({
            "mechanism": mechanism["mechanism"],
            "actor": actor,
            "object_or_scope": text,
            "source_span": evidence,
        })

    return results


def annotate_row(row: dict) -> dict:
    source = str(row.get("source_text") or "")
    language = str(row.get("language") or "").lower()

    mechanisms = []

    for rule in RULES:
        spans = []
        for pattern in rule.patterns.get(language, ()):
            spans.extend(
                collect_spans(
                    source,
                    pattern,
                    rule.mechanism,
                )
            )

        unique = []
        seen = set()
        for span in spans:
            key = (
                span["start"],
                span["end"],
                span["mechanism"],
            )
            if key not in seen:
                seen.add(key)
                unique.append(span)

        if not unique:
            continue

        mechanisms.append({
            "mechanism": rule.mechanism,
            "primary_type": rule.primary_type,
            "role": rule.role,
            "polarity": rule.polarity,
            "procedural_state": rule.procedural_state,
            "numeric_role": rule.numeric_role,
            "priority": rule.priority,
            "source_evidence": unique,
        })

    domain_candidates = [
        mechanism
        for mechanism in mechanisms
        if mechanism["role"] == "DOMAIN_MECHANISM"
        and mechanism["primary_type"]
    ]

    primary_type = ""
    primary_reason = "NO_DOMAIN_MECHANISM_CANDIDATE"

    if domain_candidates:
        domain_candidates.sort(
            key=lambda item: (
                -int(item["priority"]),
                str(item["primary_type"]),
            )
        )
        primary_type = str(
            domain_candidates[0]["primary_type"]
        )
        primary_reason = (
            "HIGHEST_PRIORITY_GROUNDED_DOMAIN_MECHANISM"
        )

    material_mechanisms = [
        mechanism["mechanism"]
        for mechanism in mechanisms
    ]

    polarity = [
        {
            "mechanism": mechanism["mechanism"],
            "polarity": mechanism["polarity"],
        }
        for mechanism in mechanisms
        if mechanism["polarity"]
    ]

    procedural_states = [
        {
            "mechanism": mechanism["mechanism"],
            "state": mechanism["procedural_state"],
        }
        for mechanism in mechanisms
        if mechanism["procedural_state"]
    ]

    evidence_spans = [
        span
        for mechanism in mechanisms
        for span in mechanism["source_evidence"]
    ]

    candidate = dict(row)
    candidate["review_status"] = "REVIEW_REQUIRED"
    candidate["reviewer"] = ""
    candidate["review_notes"] = (
        "Machine-generated gold candidate from source text only. "
        "Human legal review required before APPROVED."
    )

    candidate["candidate_gold_primary_type"] = primary_type
    candidate["candidate_gold_primary_type_reason"] = primary_reason
    candidate["candidate_gold_material_mechanisms"] = material_mechanisms
    candidate["candidate_gold_actor_object_arguments"] = (
        extract_actor_object_arguments(
            source,
            language,
            mechanisms,
        )
    )
    candidate["candidate_gold_polarity"] = polarity
    candidate["candidate_gold_procedural_states"] = procedural_states
    candidate["candidate_gold_numeric_semantic_roles"] = numeric_roles(
        source,
        language,
        mechanisms,
    )
    candidate["candidate_gold_source_evidence_spans"] = evidence_spans

    # Gold stays blank until human approval.
    candidate["gold_primary_type"] = ""
    candidate["gold_material_mechanisms"] = []
    candidate["gold_actor_object_arguments"] = []
    candidate["gold_polarity"] = []
    candidate["gold_procedural_states"] = []
    candidate["gold_numeric_semantic_roles"] = []
    candidate["gold_source_evidence_spans"] = []

    candidate["_candidate_evidence_integrity"] = all(
        valid_span(source, span)
        for span in evidence_spans
    )

    return candidate


def csv_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(
                json.dumps(row, ensure_ascii=False)
                + "\n"
            )


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "review_status",
        "reviewer",
        "review_notes",
        "language",
        "document",
        "reference",
        "title",
        "source_text",
        "pipeline_primary_type",
        "candidate_gold_primary_type",
        "candidate_gold_primary_type_reason",
        "candidate_gold_material_mechanisms",
        "candidate_gold_actor_object_arguments",
        "candidate_gold_polarity",
        "candidate_gold_procedural_states",
        "candidate_gold_numeric_semantic_roles",
        "candidate_gold_source_evidence_spans",
        "_candidate_evidence_integrity",
        "gold_primary_type",
        "gold_material_mechanisms",
        "gold_actor_object_arguments",
        "gold_polarity",
        "gold_procedural_states",
        "gold_numeric_semantic_roles",
        "gold_source_evidence_spans",
    ]

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
        )
        writer.writeheader()

        for row in rows:
            writer.writerow({
                field: csv_value(row.get(field))
                for field in fields
            })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "semantic_gold/review_pack_60_gold_candidate"
        ),
    )
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    candidates = [
        annotate_row(row)
        for row in rows
    ]

    args.out.mkdir(
        parents=True,
        exist_ok=True,
    )

    jsonl_path = (
        args.out
        / "review_pack_60_gold_candidate.jsonl"
    )
    csv_path = (
        args.out
        / "review_pack_60_gold_candidate.csv"
    )
    summary_path = (
        args.out
        / "review_pack_60_gold_candidate_summary.json"
    )

    write_jsonl(jsonl_path, candidates)
    write_csv(csv_path, candidates)

    language_counts = Counter(
        row.get("language")
        for row in candidates
    )
    candidate_type_counts = Counter(
        row.get("candidate_gold_primary_type")
        or "UNRESOLVED"
        for row in candidates
    )
    pipeline_candidate_pairs = Counter(
        (
            str(row.get("pipeline_primary_type") or ""),
            str(row.get("candidate_gold_primary_type") or "UNRESOLVED"),
        )
        for row in candidates
    )

    evidence_failures = [
        row
        for row in candidates
        if row.get("_candidate_evidence_integrity")
        is not True
    ]
    unresolved = [
        row
        for row in candidates
        if not row.get("candidate_gold_primary_type")
    ]
    primary_disagreements = [
        row
        for row in candidates
        if (
            row.get("candidate_gold_primary_type")
            and PRIMARY_TYPE_EQUIVALENCE.get(
                str(row.get("pipeline_primary_type") or ""),
                str(row.get("pipeline_primary_type") or ""),
            )
            != PRIMARY_TYPE_EQUIVALENCE.get(
                str(row.get("candidate_gold_primary_type") or ""),
                str(row.get("candidate_gold_primary_type") or ""),
            )
        )
    ]

    summary = {
        "input_rows": len(rows),
        "candidate_rows": len(candidates),
        "review_status": "REVIEW_REQUIRED",
        "languages": dict(language_counts),
        "candidate_primary_types": dict(
            candidate_type_counts.most_common()
        ),
        "unresolved_candidate_primary_type": len(
            unresolved
        ),
        "primary_type_disagreements_with_pipeline": len(
            primary_disagreements
        ),
        "candidate_evidence_integrity_failures": len(
            evidence_failures
        ),
        "pipeline_candidate_pairs": [
            {
                "pipeline": pair[0],
                "candidate": pair[1],
                "count": count,
            }
            for pair, count in (
                pipeline_candidate_pairs.most_common()
            )
        ],
        "gold_fields_approved": 0,
        "pipeline_modified": False,
        "publication_gate_modified": False,
        "human_review_required": True,
        "jsonl": str(jsonl_path),
        "csv": str(csv_path),
    }

    summary_path.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 88)
    print("SOURCE-ONLY GOLD CANDIDATE ANNOTATOR")
    print("=" * 88)
    print("INPUT ROWS:", len(rows))
    print("CANDIDATE ROWS:", len(candidates))
    print("LANGUAGES:", dict(language_counts))
    print(
        "UNRESOLVED PRIMARY TYPES:",
        len(unresolved),
    )
    print(
        "PRIMARY TYPE DISAGREEMENTS:",
        len(primary_disagreements),
    )
    print(
        "EVIDENCE INTEGRITY FAILURES:",
        len(evidence_failures),
    )
    print("APPROVED GOLD ROWS: 0")
    print("JSONL:", jsonl_path)
    print("CSV:", csv_path)
    print("SUMMARY:", summary_path)

    print("\nCANDIDATE PRIMARY TYPES")
    for clause_type, count in (
        candidate_type_counts.most_common()
    ):
        print(
            f"{count:4d}  {clause_type}"
        )

    print("\nPRIMARY TYPE DISAGREEMENTS")
    for row in primary_disagreements:
        print(
            f"{str(row.get('language')).upper()} | "
            f"{row.get('document')} | "
            f"{row.get('reference')} | "
            f"pipeline={row.get('pipeline_primary_type')} | "
            f"candidate={row.get('candidate_gold_primary_type')} | "
            f"mechanisms={row.get('candidate_gold_material_mechanisms')}"
        )

    return 2 if evidence_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
