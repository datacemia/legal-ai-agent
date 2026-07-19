#!/usr/bin/env python3
from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path

TARGET = Path("app/services/contract_agent/unified_report_from_pipeline.py")

DURATION_PATTERNS = """CONTRACT_DURATION_PATTERNS = {
    "en": (
        r"\\b(?:this\\s+)?(?:agreement|contract)\\s+shall\\s+remain\\s+in\\s+effect\\s+for\\s+([^.;\\n]{2,120})",
        r"\\b(?:this\\s+)?(?:agreement|contract)\\s+shall\\s+continue\\s+for\\s+([^.;\\n]{2,120})",
        r"\\b(?:this\\s+)?(?:agreement|contract)\\s+(?:continues?|runs?|lasts?)\\s+for\\s+([^.;\\n]{2,120})",
        r"\\b(?:this\\s+)?(?:agreement|contract)\\s+(?:expires?|ends?|terminates?)\\s+after\\s+([^.;\\n]{2,120})",
        r"\\binitial\\s+term\\s+(?:shall\\s+be|is|of|will\\s+be)\\s+([^.;\\n]{2,120})",
        r"\\b(?:the\\s+)?initial\\s+term\\s+is\\s+([^.;\\n]{2,120})",
        r"\\bterm\\s+of\\s+(?:this\\s+)?(?:agreement|contract)\\s+(?:shall\\s+be|is|will\\s+be)\\s+([^.;\\n]{2,120})",
        r"\\b(?:agreement|contract)\\s+term\\s+(?:shall\\s+be|is|of|will\\s+be)\\s+([^.;\\n]{2,120})",
    ),
    "fr": (
        r"\\b(?:le\\s+présent\\s+|le\\s+present\\s+)?(?:accord|contrat)\\s+restera\\s+en\\s+vigueur\\s+pendant\\s+([^.;\\n]{2,120})",
        r"\\b(?:le\\s+présent\\s+|le\\s+present\\s+)?(?:accord|contrat)\\s+se\\s+poursuivra\\s+pendant\\s+([^.;\\n]{2,120})",
        r"\\b(?:le\\s+présent\\s+|le\\s+present\\s+)?(?:accord|contrat)\\s+(?:est\\s+conclu|est\\s+convenu)\\s+pour\\s+(?:une\\s+)?(?:durée|duree)\\s+de\\s+([^.;\\n]{2,120})",
        r"\\b(?:le\\s+présent\\s+|le\\s+present\\s+)?(?:accord|contrat)\\s+(?:prend\\s+fin|expire)\\s+après\\s+([^.;\\n]{2,120})",
        r"\\b(?:durée|duree)\\s+initiale\\s+(?:sera|est)\\s+(?:de|à|a)\\s+([^.;\\n]{2,120})",
        r"\\b(?:la\\s+)?(?:durée|duree)\\s+(?:du\\s+|de\\s+l['’])?(?:contrat|accord)\\s+(?:est|sera)\\s+de\\s+([^.;\\n]{2,120})",
        r"\\b(?:contrat|accord)\\s+(?:d['’]une\\s+)?(?:durée|duree)\\s+de\\s+([^.;\\n]{2,120})",
    ),
    "ar": (
        r"(?:تظل|تبقى)\\s+(?:هذه\\s+)?(?:الاتفاقية|العقد)\\s+(?:سارية|نافذة)\\s+لمدة\\s+([^.;؛!؟\\n]{2,120})",
        r"(?:يستمر|تستمر|يسري|تسري)\\s+(?:هذا|هذه)?\\s*(?:العقد|الاتفاقية)\\s+لمدة\\s+([^.;؛!؟\\n]{2,120})",
        r"(?:ينتهي|تنتهي)\\s+(?:هذا|هذه)?\\s*(?:العقد|الاتفاقية)\\s+بعد\\s+([^.;؛!؟\\n]{2,120})",
        r"(?:المدة|مدة\\s+العقد|مدة\\s+الاتفاقية)\\s+الأولية\\s+(?:هي|تكون|تبلغ)\\s+([^.;؛!؟\\n]{2,120})",
        r"(?:مدة\\s+العقد|مدة\\s+الاتفاقية)\\s+(?:هي|تكون|تبلغ)\\s+([^.;؛!؟\\n]{2,120})",
        r"(?:يبرم|يُبرم|أبرم|أُبرم)\\s+(?:هذا\\s+)?(?:العقد|الاتفاقية)\\s+لمدة\\s+([^.;؛!؟\\n]{2,120})",
    ),
}"""

GENERIC_MARKERS = """GENERIC_REPORT_TEXT_MARKERS = {
    "en": (
        "this clause may create legal or operational exposure",
        "this clause should be reviewed because it may affect",
        "this clause appears administrative or operational in nature",
        "this clause is primarily administrative or definitional",
        "manual review required", "review manually",
        "source-fidelity validation", "source fidelity validation",
        "publication validation failed", "publication gate",
        "block_and_replace", "internal replacement", "blocked status",
    ),
    "fr": (
        "cette clause peut créer une exposition juridique ou opérationnelle",
        "cette clause doit être examinée car elle peut affecter",
        "cette clause semble de nature administrative ou opérationnelle",
        "cette clause est principalement administrative ou définitionnelle",
        "examen manuel requis", "revue manuelle requise",
        "révision manuelle requise", "validation de fidélité à la source",
        "validation de fidelite a la source", "fidélité à la source",
        "fidelite a la source", "échec de la validation de publication",
        "echec de la validation de publication", "publication gate",
        "block_and_replace", "remplacement interne",
        "statut bloqué", "statut bloque",
    ),
    "ar": (
        "قد ينشئ هذا البند تعرضاً قانونياً أو تشغيلياً",
        "ينبغي مراجعة هذا البند لأنه قد يؤثر",
        "يبدو هذا البند إدارياً أو تشغيلياً",
        "هذا البند إداري أو تعريفي في المقام الأول",
        "مراجعة يدوية مطلوبة", "المراجعة اليدوية مطلوبة",
        "التحقق من مطابقته للمصدر", "التحقق من مطابقة المصدر",
        "فشل التحقق من النشر", "بوابة النشر", "block_and_replace",
        "استبدال داخلي", "حالة محظورة",
    ),
}"""

ROLE_HELPER = """def normalize_published_role_text(
    value: str,
    language: str = "en",
) -> str:
    # Publication-only lexical localization. Never applied to source/quoted text.
    language = normalize_language(language)
    text = normalize_report_text(value)
    if not text:
        return ""

    if language == "fr":
        for pattern, target in (
            (r"\\\\bservice\\\\s+provider\\\\b", "Prestataire"),
            (r"\\\\bprovider\\\\b", "Prestataire"),
            (r"\\\\bcustomer\\\\b", "Client"),
            (r"\\\\bclient\\\\b", "Client"),
        ):
            text = re.sub(pattern, target, text, flags=re.IGNORECASE)
        text = re.sub(r"\\\\b[Ll]a\\\\s+(Client|Prestataire)\\\\b", r"le \\\\1", text)
        text = re.sub(r"\\\\b[Dd]e\\\\s+la\\\\s+(Client|Prestataire)\\\\b", r"du \\\\1", text)

    elif language == "ar":
        for pattern, target in (
            (r"\\\\bservice\\\\s+provider\\\\b", "مزود الخدمة"),
            (r"\\\\bprovider\\\\b", "مزود الخدمة"),
            (r"\\\\bcustomer\\\\b", "العميل"),
            (r"\\\\bclient\\\\b", "العميل"),
            (r"\\\\bprestataire\\\\b", "مزود الخدمة"),
        ):
            text = re.sub(pattern, target, text, flags=re.IGNORECASE)

    else:
        text = re.sub(r"\\\\bprestataire\\\\b", "Provider", text, flags=re.IGNORECASE)

    return normalize_report_text(text)"""

SELECTOR = """def select_clause_report_text(
    clause: dict,
    language: str = "en",
    *,
    purpose: str = "explanation",
) -> str:
    # Internal gate diagnostics are never publication candidates.
    # If a candidate fails suitability, continue; if none survives, omit.
    language = normalize_language(language)
    field_orders = {
        "explanation": (
            "explanation_simple", "why_it_matters", "legal_insight",
            "business_impact", "commercial_impact", "operational_impact",
        ),
        "risk": (
            "risk_reason", "business_impact", "commercial_impact",
            "operational_impact", "legal_insight", "explanation_simple",
            "why_it_matters",
        ),
        "action": (
            "recommendation", "negotiation_advice", "safer_alternative",
        ),
    }
    for field in field_orders.get(purpose, field_orders["explanation"]):
        value = normalize_report_text(clause.get(field, ""))
        if not value or is_generic_report_text(value, language):
            continue
        value = normalize_published_role_text(value, language)
        if value and not is_generic_report_text(value, language):
            return value
    return """""

def offsets(source, node):
    lines = source.splitlines(keepends=True)
    return (
        sum(len(x) for x in lines[:node.lineno - 1]),
        sum(len(x) for x in lines[:node.end_lineno]),
    )

def find_assignment(source, name):
    tree = ast.parse(source)
    found = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                found.append(node)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == name:
                found.append(node)
    if len(found) != 1:
        raise RuntimeError(f"{name}: expected 1 assignment, found {len(found)}")
    return offsets(source, found[0])

def find_function(source, name):
    tree = ast.parse(source)
    found = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name
    ]
    if len(found) != 1:
        raise RuntimeError(f"{name}: expected 1 function, found {len(found)}")
    return offsets(source, found[0])

def replace_span(source, span, replacement):
    a, b = span
    return source[:a] + replacement.rstrip() + source[b:]

def main():
    if not TARGET.exists():
        raise SystemExit(f"MISSING: {TARGET}")
    source = TARGET.read_text(encoding="utf-8")
    ast.parse(source)

    for anchor in (
        "CONTRACT_DURATION_PATTERNS", "GENERIC_REPORT_TEXT_MARKERS",
        "build_contract_overview", "select_clause_report_text",
    ):
        if anchor not in source:
            raise SystemExit(f"ANCHOR MISSING: {anchor}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(TARGET.name + f".before_v4_1_15_{stamp}")
    shutil.copy2(TARGET, backup)

    source = replace_span(
        source, find_assignment(source, "CONTRACT_DURATION_PATTERNS"), DURATION_PATTERNS
    )
    source = replace_span(
        source, find_assignment(source, "GENERIC_REPORT_TEXT_MARKERS"), GENERIC_MARKERS
    )

    start, _ = find_function(source, "select_clause_report_text")
    source = source[:start] + ROLE_HELPER.rstrip() + "\n\n\n" + source[start:]
    source = replace_span(
        source, find_function(source, "select_clause_report_text"), SELECTOR
    )

    old = """    duration = (
        exec_summary.get("duration")
        or overview.get("duration")
        or extract_contract_duration(contract_text, language)
    )"""
    new = """    source_duration = extract_contract_duration(
        contract_text,
        language,
    )
    duration = (
        source_duration
        or exec_summary.get("duration")
        or overview.get("duration")
    )"""
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"DURATION PRECEDENCE ANCHOR: expected 1, found {count}")
    source = source.replace(old, new, 1)

    ast.parse(source)
    TARGET.write_text(source, encoding="utf-8")

    print("=" * 96)
    print("V4.1.15 DETERMINISTIC SUMMARY HARDENING APPLIED")
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("A: EN/FR/AR source-grounded contract duration")
    print("B: internal publication diagnostics skipped; next candidate or omission")
    print("C: EN/FR/AR publication role lexical normalization")
    print("UNTOUCHED: semantic_source_profile.py, RULES, thresholds, evidence engine,")
    print("publication gate validation logic, risk weights/scoring, taxonomy, frontend")
    print("=" * 96)

if __name__ == "__main__":
    main()
