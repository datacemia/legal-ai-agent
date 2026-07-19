"""
negotiation_templates.py

International, privacy-first semantic negotiation advice helper.

Generated update:
- Keeps existing public API:
  - detect_negotiation_type(text) -> str | None
  - get_semantic_negotiation(clause, language="en") -> str
- Adds backward-compatible multi-theme helpers:
  - detect_negotiation_types(text, max_items=None) -> list[str]
  - get_semantic_negotiations(clause, language="en", max_items=3) -> list[str]

Principles:
- Standard international negotiation logic.
- Any contract / any domain.
- EN / FR / AR.
- Privacy-first: no reconstruction of real names or personal data.
"""

NEGOTIATION_TEMPLATES = {'liability': {'en': 'Consider negotiating liability caps, carve-outs for serious breaches, and '
                     'clearer exclusions for indirect or consequential damages. Also check whether '
                     'confidentiality, data protection, intellectual property, fraud, wilful '
                     'misconduct, and payment obligations should be excluded from or included '
                     'within the cap.',
               'fr': 'Envisager de négocier les plafonds de responsabilité, les exceptions pour '
                     'les violations graves et les exclusions relatives aux dommages indirects ou '
                     'consécutifs. Vérifier aussi si la confidentialité, la protection des '
                     'données, la propriété intellectuelle, la fraude, la faute intentionnelle et '
                     'les obligations de paiement doivent être incluses dans le plafond ou exclues '
                     'de celui-ci.',
               'ar': 'يمكن التفاوض على حدود المسؤولية، والاستثناءات الخاصة بالإخلالات الجسيمة، '
                     'وتوضيح استبعاد الأضرار غير المباشرة أو التبعية. وينبغي أيضاً مراجعة ما إذا '
                     'كانت السرية أو حماية البيانات أو الملكية الفكرية أو الغش أو الخطأ العمدي أو '
                     'التزامات الدفع يجب أن تكون داخل حد المسؤولية أو خارجه.'},
 'confidentiality': {'en': 'Consider narrowing the scope of confidential information, adding '
                           'standard disclosure exceptions, clarifying permitted recipients, and '
                           'limiting the duration of post-termination confidentiality obligations '
                           'based on the sensitivity of the information.',
                     'fr': 'Envisager de restreindre le périmètre des informations '
                           'confidentielles, d’ajouter des exceptions usuelles de divulgation, de '
                           'clarifier les destinataires autorisés et de limiter la durée des '
                           'obligations de confidentialité après la fin du contrat selon la '
                           'sensibilité des informations.',
                     'ar': 'يمكن التفاوض على تضييق نطاق المعلومات السرية، وإضافة استثناءات إفصاح '
                           'معتادة، وتوضيح الجهات المسموح لها بالاطلاع، وتحديد مدة الالتزام '
                           'بالسرية بعد انتهاء العقد حسب حساسية المعلومات.'},
 'termination': {'en': 'Consider negotiating longer cure periods, clearer breach definitions, '
                       'reciprocal termination rights, transition assistance, payment '
                       'consequences, and a clear list of obligations that survive termination.',
                 'fr': 'Envisager de négocier des délais de régularisation plus longs, des '
                       'définitions plus précises des manquements, des droits de résiliation '
                       'réciproques, une assistance de transition, les conséquences de paiement et '
                       'une liste claire des obligations qui survivent à la résiliation.',
                 'ar': 'يمكن التفاوض على تمديد مهلة المعالجة، وتوضيح حالات الإخلال، وإضافة حقوق '
                       'إنهاء متبادلة، وتنظيم المساعدة الانتقالية، وآثار الدفع، وقائمة واضحة '
                       'بالالتزامات التي تستمر بعد انتهاء العقد.'},
 'payment': {'en': 'Consider negotiating payment deadlines, grace periods, late-payment interest, '
                   'invoice dispute procedures, tax treatment, currency, set-off rights, and '
                   'suspension rights for unpaid amounts.',
             'fr': 'Envisager de négocier les délais de paiement, les délais de grâce, les '
                   'intérêts de retard, les procédures de contestation des factures, le traitement '
                   'fiscal, la devise, les droits de compensation et les droits de suspension en '
                   'cas de sommes impayées.',
             'ar': 'يمكن التفاوض على آجال الدفع، وفترات السماح، وفوائد التأخير، وإجراءات الاعتراض '
                   'على الفواتير، والمعالجة الضريبية، والعملة، وحقوق المقاصة، وحقوق تعليق '
                   'الالتزامات عند عدم السداد.'},
 'data_protection': {'en': 'Consider clarifying security measures, processing instructions, breach '
                           'notification timelines, audit rights, subprocessor controls, data '
                           'return or deletion duties, cross-border transfers, and allocation of '
                           'regulatory responsibility.',
                     'fr': 'Envisager de clarifier les mesures de sécurité, les instructions de '
                           'traitement, les délais de notification des violations, les droits '
                           'd’audit, le contrôle des sous-traitants, les obligations de '
                           'restitution ou suppression des données, les transferts internationaux '
                           'et la répartition des responsabilités réglementaires.',
                     'ar': 'يمكن التفاوض على توضيح تدابير الأمن، وتعليمات المعالجة، ومهل الإشعار '
                           'بالاختراقات، وحقوق التدقيق، وضوابط المعالجين الفرعيين، وواجبات إعادة '
                           'البيانات أو حذفها، ونقل البيانات عبر الحدود، وتوزيع المسؤوليات '
                           'التنظيمية.'},
 'service_level': {'en': 'Consider negotiating measurable uptime commitments, service credits, '
                         'measurement periods, exclusions, reporting duties, incident response '
                         'timelines, escalation procedures, and termination rights for repeated '
                         'service failures.',
                   'fr': 'Envisager de négocier des engagements de disponibilité mesurables, des '
                         'crédits de service, les périodes de mesure, les exclusions, les '
                         'obligations de reporting, les délais de réponse aux incidents, les '
                         'procédures d’escalade et les droits de résiliation en cas d’échecs '
                         'répétés du service.',
                   'ar': 'يمكن التفاوض على التزامات توفر قابلة للقياس، وائتمانات خدمة، وفترات '
                         'القياس، والاستثناءات، والتقارير، ومهل الاستجابة للحوادث، وإجراءات '
                         'التصعيد، وحقوق الإنهاء عند تكرار فشل الخدمة.'},
 'governing_law': {'en': 'Consider negotiating the governing law, dispute forum, arbitration '
                         'mechanism, venue, language of proceedings, interim relief options, and '
                         'whether the chosen forum is practical for enforcement and access.',
                   'fr': 'Envisager de négocier la loi applicable, le tribunal compétent, le '
                         'mécanisme d’arbitrage, le lieu de règlement des litiges, la langue de '
                         'procédure, les mesures provisoires et le caractère pratique du forum '
                         'choisi pour l’exécution et l’accès.',
                   'ar': 'يمكن التفاوض على القانون الواجب التطبيق، والجهة المختصة، وآلية التحكيم، '
                         'ومكان النزاع، ولغة الإجراءات، والتدابير المؤقتة، ومدى ملاءمة الجهة '
                         'المختارة للتنفيذ والوصول العملي.'},
 'intellectual_property': {'en': 'Consider clarifying ownership, permitted use, licensing scope, '
                                 'background IP, newly created deliverables, improvements, '
                                 'derivative works, approval rights, moral rights, transfer '
                                 'timing, and post-termination restrictions.',
                           'fr': 'Envisager de clarifier la propriété, les usages autorisés, '
                                 'l’étendue de la licence, la propriété intellectuelle '
                                 'préexistante, les livrables créés, les améliorations, les œuvres '
                                 'dérivées, les droits d’approbation, les droits moraux, le moment '
                                 'du transfert et les restrictions après la fin du contrat.',
                           'ar': 'يمكن التفاوض على توضيح الملكية، والاستخدامات المسموح بها، ونطاق '
                                 'الترخيص، والملكية الفكرية السابقة، والمخرجات المنشأة، '
                                 'والتحسينات، والأعمال المشتقة، وحقوق الموافقة، والحقوق المعنوية، '
                                 'وتوقيت النقل، والقيود بعد انتهاء العقد.'},
 'restrictive_covenants': {'en': 'Consider limiting the scope, duration, territory, restricted '
                                 'activities, covered customers or personnel, and remedies for '
                                 'restrictive covenants. The restriction should be tied to a '
                                 'legitimate commercial interest and should include clear '
                                 'carve-outs for ordinary business activity.',
                           'fr': 'Envisager de limiter la portée, la durée, le territoire, les '
                                 'activités restreintes, les clients ou personnes concernés et les '
                                 'recours liés aux clauses restrictives. La restriction devrait '
                                 'être liée à un intérêt commercial légitime et prévoir des '
                                 'exceptions claires pour l’activité ordinaire.',
                           'ar': 'يمكن التفاوض على تقليص نطاق القيود ومدتها ونطاقها الجغرافي '
                                 'والأنشطة المقيدة والعملاء أو الأشخاص المعنيين ووسائل الانتصاف. '
                                 'وينبغي ربط القيد بمصلحة تجارية مشروعة مع استثناءات واضحة للنشاط '
                                 'التجاري العادي.'},
 'assignment': {'en': 'Consider requiring prior written consent for assignment, transfer or '
                      'delegation, while allowing reasonable exceptions for affiliates, group '
                      'restructuring, mergers, acquisitions, or sale of substantially all assets '
                      'where the assignee can perform the obligations.',
                'fr': 'Envisager d’exiger un consentement écrit préalable pour toute cession, '
                      'transfert ou délégation, tout en prévoyant des exceptions raisonnables pour '
                      'les affiliés, les restructurations de groupe, les fusions, acquisitions ou '
                      'cessions de la quasi-totalité des actifs lorsque le cessionnaire peut '
                      'exécuter les obligations.',
                'ar': 'يمكن التفاوض على اشتراط الموافقة الخطية المسبقة على أي تنازل أو نقل أو '
                      'تفويض، مع السماح باستثناءات معقولة للشركات التابعة أو إعادة الهيكلة أو '
                      'الاندماج أو الاستحواذ أو بيع معظم الأصول إذا كان المتنازل له قادراً على '
                      'تنفيذ الالتزامات.'},
 'audit': {'en': 'Consider defining audit scope, frequency, notice, confidentiality, access to '
                 'records, use of third-party auditors, remediation timelines, and who bears audit '
                 'costs.',
           'fr': 'Envisager de définir le périmètre de l’audit, sa fréquence, le préavis, la '
                 'confidentialité, l’accès aux registres, le recours à des auditeurs tiers, les '
                 'délais de correction et la partie qui supporte les coûts de l’audit.',
           'ar': 'يمكن التفاوض على نطاق التدقيق وتكراره والإشعار والسرية والوصول إلى السجلات '
                 'واستخدام مدققين خارجيين ومهل المعالجة ومن يتحمل تكاليف التدقيق.'},
 'insurance': {'en': 'Consider negotiating minimum coverage levels, policy types, evidence of '
                     'insurance, notice of cancellation, deductibles, exclusions, additional '
                     'insured status, and whether coverage aligns with the contract risk.',
               'fr': 'Envisager de négocier les niveaux minimaux de couverture, les types de '
                     'polices, les justificatifs d’assurance, le préavis d’annulation, les '
                     'franchises, les exclusions, le statut d’assuré additionnel et l’adéquation '
                     'de la couverture avec les risques du contrat.',
               'ar': 'يمكن التفاوض على الحد الأدنى للتغطية، وأنواع وثائق التأمين، وإثبات التأمين، '
                     'والإشعار بالإلغاء، والتحملات، والاستثناءات، وإضافة طرف كمؤمن له إضافي، ومدى '
                     'توافق التغطية مع مخاطر العقد.'},
 'delivery_acceptance': {'en': 'Consider negotiating objective acceptance criteria, delivery '
                               'milestones, testing procedures, rejection rights, cure periods, '
                               'deemed acceptance, re-delivery obligations, and payment links to '
                               'acceptance.',
                         'fr': 'Envisager de négocier des critères objectifs de réception, des '
                               'jalons de livraison, des procédures de test, des droits de rejet, '
                               'des délais de correction, l’acceptation tacite, les obligations de '
                               'nouvelle livraison et le lien entre paiement et acceptation.',
                         'ar': 'يمكن التفاوض على معايير قبول موضوعية، ومراحل التسليم، وإجراءات '
                               'الاختبار، وحقوق الرفض، ومهل المعالجة، والقبول الضمني، والتزامات '
                               'إعادة التسليم، وربط الدفع بالقبول.'},
 'governance_compliance': {'en': 'Consider clarifying governance responsibilities, compliance '
                                 'standards, reporting obligations, approval rights, '
                                 'subcontracting controls, sanctions compliance, anti-bribery '
                                 'obligations, and consequences for non-compliance.',
                           'fr': 'Envisager de clarifier les responsabilités de gouvernance, les '
                                 'standards de conformité, les obligations de reporting, les '
                                 'droits d’approbation, le contrôle de la sous-traitance, la '
                                 'conformité aux sanctions, les obligations anticorruption et les '
                                 'conséquences du non-respect.',
                           'ar': 'يمكن التفاوض على توضيح مسؤوليات الحوكمة، ومعايير الامتثال، '
                                 'والتقارير، وحقوق الموافقة، وضوابط التعاقد من الباطن، والامتثال '
                                 'للعقوبات، والتزامات مكافحة الرشوة، وآثار عدم الامتثال.'},
 'change_of_control': {'en': 'Consider defining what counts as a change of control, whether prior '
                             'consent or notice is required, whether termination rights are '
                             'triggered, and whether payments, vesting, assignment, '
                             'confidentiality, or service continuity are affected.',
                       'fr': 'Envisager de définir ce qui constitue un changement de contrôle, si '
                             'un consentement préalable ou une notification est requis, si un '
                             'droit de résiliation est déclenché et si les paiements, '
                             'l’acquisition de droits, la cession, la confidentialité ou la '
                             'continuité du service sont affectés.',
                       'ar': 'يمكن التفاوض على تعريف تغيير السيطرة، وما إذا كانت الموافقة المسبقة '
                             'أو الإشعار مطلوباً، وما إذا كان ذلك يفعّل حق الإنهاء، وما إذا كان '
                             'يؤثر على المدفوعات أو الاستحقاق أو التنازل أو السرية أو استمرارية '
                             'الخدمة.'},
 'real_estate': {'en': 'Consider negotiating rent review, deposit handling, permitted use, '
                       'repairs, maintenance, utilities, insurance, access rights, renewal, '
                       'termination, handover condition, and allocation of property-related costs.',
                 'fr': 'Envisager de négocier la révision du loyer, le traitement du dépôt, '
                       'l’usage autorisé, les réparations, l’entretien, les charges, l’assurance, '
                       'les droits d’accès, le renouvellement, la résiliation, l’état de '
                       'restitution et la répartition des coûts liés au bien.',
                 'ar': 'يمكن التفاوض على مراجعة الأجرة، ومعالجة الوديعة، والاستخدام المسموح، '
                       'والإصلاحات، والصيانة، والمرافق، والتأمين، وحقوق الدخول، والتجديد، '
                       'والإنهاء، وحالة التسليم، وتوزيع التكاليف المتعلقة بالعقار.'},
 'finance_lending': {'en': 'Consider negotiating financial covenants, events of default, cure '
                           'rights, repayment flexibility, interest, fees, security, guarantees, '
                           'acceleration, reporting duties, and enforcement mechanics.',
                     'fr': 'Envisager de négocier les engagements financiers, les cas de défaut, '
                           'les droits de régularisation, la flexibilité de remboursement, les '
                           'intérêts, les frais, les sûretés, les garanties, l’exigibilité '
                           'anticipée, les obligations de reporting et les mécanismes d’exécution.',
                     'ar': 'يمكن التفاوض على التعهدات المالية، وحالات التعثر، وحقوق المعالجة، '
                           'ومرونة السداد، والفوائد، والرسوم، والضمانات، والكفالات، والتعجيل '
                           'بالاستحقاق، والتقارير، وآليات التنفيذ.'},
 'force_majeure': {'en': 'Consider defining qualifying force majeure events, notice obligations, '
                         'mitigation duties, suspension periods, termination rights, evidence '
                         'requirements, and allocation of costs after prolonged disruption.',
                   'fr': 'Envisager de définir les événements constitutifs de force majeure, les '
                         "obligations de notification, les mesures d'atténuation, les périodes de "
                         'suspension, les droits de résiliation, les exigences de preuve et la '
                         'répartition des coûts en cas de perturbation prolongée.',
                   'ar': 'يمكن التفاوض على تحديد أحداث القوة القاهرة، وواجبات الإشعار، وواجبات '
                         'التخفيف، وفترات التعليق، وحقوق الإنهاء، ومتطلبات الإثبات، وتوزيع '
                         'التكاليف عند استمرار التعطيل لفترة طويلة.'},
 'warranties': {'en': 'Consider clarifying representations and warranties, quality standards, '
                      'disclaimers, exclusions, remedy periods, reliance limitations, and how '
                      'warranty remedies interact with limitation of liability.',
                'fr': 'Envisager de clarifier les déclarations et garanties, les standards de '
                      'qualité, les exclusions, les délais de recours, les limites de confiance '
                      "accordée aux déclarations et l'interaction entre les recours de garantie et "
                      'la limitation de responsabilité.',
                'ar': 'يمكن التفاوض على توضيح الإقرارات والضمانات، ومعايير الجودة، والاستثناءات، '
                      'ومدد المعالجة، وحدود الاعتماد على الإقرارات، وعلاقة وسائل الانتصاف الخاصة '
                      'بالضمان بحدود المسؤولية.'},
 'notices': {'en': 'Consider defining notice methods, required addresses, deemed receipt, '
                   'electronic delivery, language requirements, emergency notices, and '
                   'change-of-address procedures.',
             'fr': 'Envisager de définir les modes de notification, les adresses requises, la '
                   'réception réputée, la notification électronique, les exigences linguistiques, '
                   "les notifications urgentes et les procédures de changement d'adresse.",
             'ar': 'يمكن التفاوض على تحديد وسائل الإشعار، والعناوين المطلوبة، والاستلام الحكمي، '
                   'والإشعار الإلكتروني، ومتطلبات اللغة، والإشعارات العاجلة، وإجراءات تغيير '
                   'العنوان.'},
 'tax': {'en': 'Consider clarifying taxes, VAT/GST, withholding, gross-up obligations, tax '
               'documentation, invoicing responsibilities, and allocation of tax risk.',
         'fr': 'Envisager de clarifier les impôts, la TVA ou taxes similaires, les retenues à la '
               'source, les clauses de majoration, les documents fiscaux, les responsabilités de '
               'facturation et la répartition du risque fiscal.',
         'ar': 'يمكن التفاوض على توضيح الضرائب، وضريبة القيمة المضافة أو ما يعادلها، والاستقطاعات، '
               'والتعويض الضريبي، والمستندات الضريبية، ومسؤوليات الفوترة، وتوزيع المخاطر '
               'الضريبية.'},
 'entire_agreement': {'en': 'Consider confirming what prior statements, proposals, schedules, '
                            'order forms, exhibits, or side letters are superseded or preserved, '
                            'and whether fraud or intentional misrepresentation carve-outs are '
                            'needed.',
                      'fr': 'Envisager de confirmer quelles déclarations, propositions, annexes, '
                            'bons de commande, pièces jointes ou lettres annexes antérieurs sont '
                            'remplacés ou préservés, et si des exceptions pour fraude ou fausse '
                            'déclaration intentionnelle sont nécessaires.',
                      'ar': 'يمكن التفاوض على تحديد ما إذا كانت التصريحات أو العروض أو الجداول أو '
                            'نماذج الطلب أو الملاحق أو الرسائل الجانبية السابقة مستبدلة أو محفوظة، '
                            'وما إذا كانت هناك حاجة لاستثناءات تتعلق بالغش أو التصريحات المضللة '
                            'العمدية.'},
 'amendment': {'en': 'Consider requiring written amendments, authorized signatories, version '
                     'control, change-order procedures, and rules for operational or technical '
                     'updates.',
               'fr': "Envisager d'exiger des modifications écrites, des signataires autorisés, un "
                     "contrôle des versions, des procédures d'ordre de modification et des règles "
                     'pour les mises à jour opérationnelles ou techniques.',
               'ar': 'يمكن التفاوض على اشتراط التعديلات الخطية، والموقعين المفوضين، وضبط '
                     'الإصدارات، وإجراءات أوامر التغيير، وقواعد التحديثات التشغيلية أو التقنية.'},
 'waiver': {'en': 'Consider clarifying that failure or delay in enforcing a right does not waive '
                  'that right, and that waivers must be written, specific, and limited.',
            'fr': "Envisager de préciser que le défaut ou le retard dans l'exercice d'un droit ne "
                  'vaut pas renonciation, et que toute renonciation doit être écrite, spécifique '
                  'et limitée.',
            'ar': 'يمكن التفاوض على توضيح أن عدم ممارسة الحق أو التأخر في ممارسته لا يعد تنازلاً '
                  'عنه، وأن أي تنازل يجب أن يكون خطياً ومحدداً ومحدود النطاق.'},
 'severability': {'en': 'Consider clarifying whether invalid provisions are severed, replaced with '
                        'valid equivalents, or renegotiated, and how this affects the remaining '
                        'agreement.',
                  'fr': 'Envisager de préciser si les clauses invalides sont séparées, remplacées '
                        'par des clauses valides équivalentes ou renégociées, et comment cela '
                        'affecte le reste du contrat.',
                  'ar': 'يمكن التفاوض على توضيح ما إذا كانت الأحكام غير الصحيحة تُفصل أو تُستبدل '
                        'بأحكام صحيحة مكافئة أو يُعاد التفاوض بشأنها، وكيف يؤثر ذلك على باقي '
                        'العقد.'},
 'survival': {'en': 'Consider listing which obligations survive termination or expiry, including '
                    'confidentiality, payment, audit, data return, IP, dispute resolution, and '
                    'liability provisions.',
              'fr': "Envisager d'énumérer les obligations qui survivent à la résiliation ou à "
                    "l'expiration, notamment la confidentialité, le paiement, l'audit, la "
                    'restitution des données, la propriété intellectuelle, le règlement des '
                    'litiges et la responsabilité.',
              'ar': 'يمكن التفاوض على تحديد الالتزامات التي تستمر بعد الإنهاء أو الانقضاء، بما في '
                    'ذلك السرية، والدفع، والتدقيق، وإعادة البيانات، والملكية الفكرية، وتسوية '
                    'النزاعات، وأحكام المسؤولية.'},
 'renewal': {'en': 'Consider clarifying renewal mechanics, notice windows, automatic renewal, '
                   'pricing changes, termination before renewal, and any service or payment '
                   'changes.',
             'fr': 'Envisager de clarifier les mécanismes de renouvellement, les fenêtres de '
                   'préavis, la reconduction automatique, les changements de prix, la résiliation '
                   'avant renouvellement et les changements de service ou de paiement.',
             'ar': 'يمكن التفاوض على توضيح آليات التجديد، ومهل الإشعار، والتجديد التلقائي، '
                   'وتغييرات الأسعار، والإنهاء قبل التجديد، وأي تغييرات في الخدمة أو الدفع.'},
 'suspension': {'en': 'Consider defining when suspension is allowed, required notice, cure rights, '
                      'service continuity protections, data access during suspension, and '
                      'reinstatement conditions.',
                'fr': 'Envisager de définir les cas de suspension, le préavis requis, les droits '
                      "de régularisation, les protections de continuité, l'accès aux données "
                      'pendant la suspension et les conditions de rétablissement.',
                'ar': 'يمكن التفاوض على تحديد حالات التعليق، والإشعار المطلوب، وحقوق المعالجة، '
                      'وضمانات استمرارية الخدمة، والوصول إلى البيانات أثناء التعليق، وشروط '
                      'الاستئناف.'}}

NEGOTIATION_ALIASES = {'services_operations': 'service_level',
 'sla': 'service_level',
 'service_levels': 'service_level',
 'data_privacy_security': 'data_protection',
 'privacy': 'data_protection',
 'ip': 'intellectual_property',
 'dispute_resolution': 'governing_law',
 'arbitration': 'governing_law',
 'venue': 'governing_law',
 'jurisdiction': 'governing_law',
 'restrictive': 'restrictive_covenants',
 'non_compete': 'restrictive_covenants',
 'non_solicitation': 'restrictive_covenants',
 'compliance': 'governance_compliance',
 'governance': 'governance_compliance',
 'lending': 'finance_lending',
 'loan': 'finance_lending',
 'lease': 'real_estate',
 'force majeure': 'force_majeure',
 'act_of_god': 'force_majeure',
 'warranty': 'warranties',
 'warranties': 'warranties',
 'representations': 'warranties',
 'representations_and_warranties': 'warranties',
 'notice': 'notices',
 'notices': 'notices',
 'taxation': 'tax',
 'taxes': 'tax',
 'entire agreement': 'entire_agreement',
 'entire_agreement_clause': 'entire_agreement',
 'amendments': 'amendment',
 'modification': 'amendment',
 'waivers': 'waiver',
 'severability_clause': 'severability',
 'surviving_obligations': 'survival',
 'auto_renewal': 'renewal',
 'automatic_renewal': 'renewal',
 'service_suspension': 'suspension'}

ORDERED_NEGOTIATION_SIGNALS = [('liability',
  ['limitation of liability',
   'liability cap',
   'unlimited liability',
   'liability',
   'indemnity',
   'indemnification',
   'responsabilité',
   'limitation de responsabilité',
   'plafond de responsabilité',
   'indemnisation',
   'المسؤولية',
   'تحديد المسؤولية',
   'حد المسؤولية',
   'تعويض']),
 ('data_protection',
  ['data protection',
   'personal data',
   'data processing',
   'security measures',
   'breach notification',
   'security incident',
   'subprocessor',
   'protection des données',
   'données personnelles',
   'traitement des données',
   'mesures de sécurité',
   'incident de sécurité',
   'sous-traitant',
   'حماية البيانات',
   'البيانات الشخصية',
   'معالجة البيانات',
   'الأمن السيبراني',
   'حادث أمني',
   'معالج فرعي']),
 ('service_level',
  ['service level',
   'service levels',
   'sla',
   'uptime',
   'availability',
   'service credits',
   'service credit',
   'niveau de service',
   'disponibilité',
   'crédit de service',
   'مستوى الخدمة',
   'التوفر',
   'التوافر',
   'تعويض الخدمة']),
 ('restrictive_covenants',
  ['non-compete',
   'non compete',
   'non-solicitation',
   'non solicitation',
   'non-circumvention',
   'exclusivity',
   'exclusive dealing',
   'non-concurrence',
   'non-sollicitation',
   'non-contournement',
   'exclusivité',
   'عدم المنافسة',
   'عدم الاستقطاب',
   'عدم الالتفاف',
   'الحصرية']),
 ('confidentiality',
  ['confidentiality',
   'confidential information',
   'trade secret',
   'non-disclosure',
   'confidentialité',
   'informations confidentielles',
   'secret commercial',
   'non-divulgation',
   'السرية',
   'معلومات سرية',
   'سر تجاري',
   'عدم الإفصاح']),
 ('termination',
  ['termination',
   'terminate',
   'cure period',
   'material breach',
   'notice period',
   'post-termination',
   'résiliation',
   'préavis',
   'manquement',
   'délai de régularisation',
   'après résiliation',
   'فسخ',
   'إنهاء',
   'إشعار',
   'إخلال جوهري',
   'مهلة معالجة',
   'بعد الإنهاء']),
 ('payment',
  ['payment',
   'fees',
   'invoice',
   'late payment',
   'rent',
   'price',
   'royalty',
   'commission',
   'paiement',
   'loyer',
   'facture',
   'intérêts de retard',
   'prix',
   'redevance',
   'commission',
   'الدفع',
   'الرسوم',
   'الفاتورة',
   'فوائد التأخير',
   'الكراء',
   'السداد',
   'ثمن',
   'إتاوة',
   'عمولة']),
 ('governing_law',
  ['governing law',
   'jurisdiction',
   'arbitration',
   'venue',
   'mediation',
   'court',
   'droit applicable',
   'tribunal compétent',
   'arbitrage',
   'médiation',
   'juridiction',
   'القانون الواجب التطبيق',
   'المحكمة المختصة',
   'التحكيم',
   'وساطة',
   'اختصاص']),
 ('intellectual_property',
  ['intellectual property',
   'trademark',
   'license',
   'licence',
   'ownership',
   'assignment of ip',
   'work product',
   'deliverables',
   'propriété intellectuelle',
   'marque',
   'licence',
   'propriété',
   'livrables',
   'الملكية الفكرية',
   'العلامات التجارية',
   'ترخيص',
   'ملكية',
   'مخرجات العمل']),
 ('assignment',
  ['assignment',
   'assign',
   'transfer',
   'delegate',
   'cession',
   'céder',
   'transfert',
   'déléguer',
   'تنازل',
   'نقل',
   'تفويض']),
 ('audit',
  ['audit',
   'inspection',
   'records',
   'books',
   'access to records',
   'audit',
   'inspection',
   'registres',
   'accès aux registres',
   'تدقيق',
   'تفتيش',
   'سجلات',
   'الوصول إلى السجلات']),
 ('insurance',
  ['insurance',
   'policy',
   'coverage',
   'certificate of insurance',
   'assurance',
   'police',
   'couverture',
   "attestation d'assurance",
   'تأمين',
   'وثيقة التأمين',
   'تغطية',
   'شهادة تأمين']),
 ('delivery_acceptance',
  ['delivery',
   'deliverable',
   'acceptance',
   'acceptance criteria',
   'testing',
   'milestone',
   'livraison',
   'livrable',
   'réception',
   'acceptation',
   "critères d'acceptation",
   'test',
   'jalon',
   'تسليم',
   'مخرج',
   'قبول',
   'معايير القبول',
   'اختبار',
   'مرحلة']),
 ('governance_compliance',
  ['compliance',
   'sanctions',
   'anti-bribery',
   'approval',
   'consent',
   'subcontracting',
   'governance',
   'conformité',
   'sanctions',
   'lutte contre la corruption',
   'approbation',
   'consentement',
   'sous-traitance',
   'gouvernance',
   'امتثال',
   'عقوبات',
   'مكافحة الرشوة',
   'موافقة',
   'تعاقد من الباطن',
   'حوكمة']),
 ('change_of_control',
  ['change of control',
   'merger',
   'acquisition',
   'sale of substantially all assets',
   'changement de contrôle',
   'fusion',
   'acquisition',
   'cession de la quasi-totalité des actifs',
   'تغيير السيطرة',
   'اندماج',
   'استحواذ',
   'بيع معظم الأصول']),
 ('real_estate',
  ['lease',
   'rent',
   'premises',
   'tenant',
   'landlord',
   'deposit',
   'bail',
   'loyer',
   'locaux',
   'locataire',
   'bailleur',
   'dépôt',
   'إيجار',
   'أجرة',
   'عقار',
   'مستأجر',
   'مؤجر',
   'وديعة']),
 ('finance_lending',
  ['loan',
   'credit facility',
   'borrower',
   'lender',
   'interest',
   'collateral',
   'security interest',
   'prêt',
   'crédit',
   'emprunteur',
   'prêteur',
   'intérêt',
   'garantie',
   'sûreté',
   'قرض',
   'تسهيل ائتماني',
   'مقترض',
   'مقرض',
   'فائدة',
   'ضمان']),
 ('force_majeure',
  ['force majeure',
   'act of god',
   'unforeseeable event',
   'beyond reasonable control',
   'cas de force majeure',
   'événement imprévisible',
   'hors du contrôle raisonnable',
   'القوة القاهرة',
   'حدث غير متوقع',
   'خارج السيطرة المعقولة']),
 ('warranties',
  ['warranty',
   'warranties',
   'representation',
   'representations and warranties',
   'as is',
   'disclaimer of warranty',
   'garantie',
   'garanties',
   'déclaration',
   'déclarations et garanties',
   "en l'état",
   'exclusion de garantie',
   'ضمان',
   'ضمانات',
   'إقرار',
   'الإقرارات والضمانات',
   'كما هو',
   'استبعاد الضمان']),
 ('notices',
  ['notice',
   'notices',
   'deemed receipt',
   'electronic notice',
   'address for notice',
   'notification',
   'notifications',
   'réception réputée',
   'adresse de notification',
   'إشعار',
   'إخطارات',
   'الاستلام الحكمي',
   'الإشعار الإلكتروني',
   'عنوان الإشعار']),
 ('tax',
  ['tax',
   'taxes',
   'vat',
   'gst',
   'withholding',
   'gross-up',
   'tax invoice',
   'impôt',
   'impôts',
   'tva',
   'retenue à la source',
   'majoration fiscale',
   'ضريبة',
   'ضرائب',
   'القيمة المضافة',
   'اقتطاع',
   'تعويض ضريبي',
   'فاتورة ضريبية']),
 ('entire_agreement',
  ['entire agreement',
   'entire understanding',
   'integration clause',
   'supersedes all prior',
   "intégralité de l'accord",
   'intégralité du contrat',
   'remplace tous les accords antérieurs',
   'الاتفاق الكامل',
   'كامل الاتفاق',
   'يحل محل جميع الاتفاقات السابقة']),
 ('amendment',
  ['amendment',
   'amendments',
   'modified only in writing',
   'change order',
   'modification',
   'avenant',
   'modifié uniquement par écrit',
   'ordre de modification',
   'تعديل',
   'تعديلات',
   'لا يعدل إلا كتابة',
   'أمر تغيير']),
 ('waiver',
  ['waiver',
   'no waiver',
   'failure to enforce',
   'delay in exercising',
   'renonciation',
   'absence de renonciation',
   "défaut d'exercice",
   "retard dans l'exercice",
   'تنازل',
   'عدم التنازل',
   'عدم ممارسة الحق',
   'التأخر في ممارسة الحق']),
 ('severability',
  ['severability',
   'invalid provision',
   'unenforceable provision',
   'severed',
   'divisibilité',
   'clause invalide',
   'clause inapplicable',
   'séparée',
   'قابلية الفصل',
   'حكم غير صحيح',
   'حكم غير قابل للتنفيذ',
   'فصل الحكم']),
 ('survival',
  ['survival',
   'survive termination',
   'survive expiry',
   'post-termination obligations',
   'survie',
   'survivent à la résiliation',
   'obligations postérieures à la résiliation',
   'استمرار',
   'تستمر بعد الإنهاء',
   'التزامات ما بعد الإنهاء']),
 ('renewal',
  ['renewal',
   'automatic renewal',
   'auto-renewal',
   'renewal term',
   'renouvellement',
   'reconduction automatique',
   'période de renouvellement',
   'تجديد',
   'تجديد تلقائي',
   'مدة التجديد']),
 ('suspension',
  ['suspension',
   'suspend services',
   'service suspension',
   'reinstatement',
   'suspension',
   'suspendre les services',
   'rétablissement',
   'تعليق',
   'تعليق الخدمات',
   'استئناف الخدمة'])]

SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_negotiation_type(negotiation_type: str) -> str:
    value = str(negotiation_type or "").lower().strip()
    return NEGOTIATION_ALIASES.get(value, value)


def unique_preserve_order(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def detect_negotiation_types(
    text: str,
    max_items: int | None = None,
) -> list[str]:
    """
    Detect all relevant negotiation themes in a clause.

    This is privacy-first: it only inspects anonymized/legal text and does
    not attempt to infer or reconstruct real identities.
    """
    normalized = str(text or "").lower()
    matches = []

    for negotiation_type, signals in ORDERED_NEGOTIATION_SIGNALS:
        if any(str(signal or "").lower() in normalized for signal in signals):
            normalized_type = normalize_negotiation_type(negotiation_type)

            if normalized_type in NEGOTIATION_TEMPLATES:
                matches.append(normalized_type)

    matches = unique_preserve_order(matches)

    if max_items is not None:
        try:
            max_items = int(max_items)
        except Exception:
            max_items = 0

        return matches[:max(0, max_items)]

    return matches


def detect_negotiation_type(text: str) -> str | None:
    """
    Backward-compatible single-theme detector.
    Returns the first detected type using ordered priority.
    """
    matches = detect_negotiation_types(text, max_items=1)
    return matches[0] if matches else None


def build_clause_text_for_negotiation(clause: dict) -> str:
    if not isinstance(clause, dict):
        return ""

    return " ".join([
        str(clause.get("clause_title", "")),
        str(clause.get("title", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("original_text", "")),
        str(clause.get("clause_text", "")),
        str(clause.get("text", "")),
        str(clause.get("explanation_simple", "")),
        str(clause.get("legal_insight", "")),
    ])


def get_semantic_negotiations(
    clause: dict,
    language: str = "en",
    max_items: int = 3,
) -> list[str]:
    """
    Extended multi-theme advice.
    Keeps output concise by default while supporting hybrid clauses such as
    liability + confidentiality + data protection.
    """
    language = normalize_language(language)

    if not isinstance(clause, dict):
        return []

    explicit_type = (
        clause.get("negotiation_type")
        or clause.get("clause_type")
        or clause.get("type")
    )

    explicit_type = normalize_negotiation_type(explicit_type)

    negotiation_types = []

    if explicit_type in NEGOTIATION_TEMPLATES:
        negotiation_types.append(explicit_type)

    negotiation_types.extend(
        detect_negotiation_types(
            build_clause_text_for_negotiation(clause),
            max_items=None,
        )
    )

    negotiation_types = unique_preserve_order(negotiation_types)

    results = []

    for negotiation_type in negotiation_types[:max(1, int(max_items or 1))]:
        template = NEGOTIATION_TEMPLATES.get(negotiation_type, {})
        advice = template.get(language, template.get("en", ""))

        if advice:
            results.append(advice)

    return results


def get_semantic_negotiation(
    clause: dict,
    language: str = "en",
) -> str:
    """
    Backward-compatible single advice string.
    """
    results = get_semantic_negotiations(
        clause,
        language=language,
        max_items=1,
    )

    return results[0] if results else ""
