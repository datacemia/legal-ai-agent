"use client";

import RiskBadge from "./RiskBadge";

type Props = {
  result: any;
  language: string;
  showGraphs?: boolean;
};

const DASHBOARD_TRANSLATIONS: any = {
  en: {
    highRisk: "High Risk",
    mediumRisk: "Medium Risk",
    lowRisk: "Low Risk",
    contradictions: "Contradictions",
    dependencies: "Dependencies",
    riskHeatmap: "Risk Heatmap",
    topRisks: "Top Risks",
    executiveNarrative: "Executive Narrative",
    dependencyGraph: "Dependency Graph",
    legalRelationGraph: "Legal Relation Graph",
    clauseGroups: "Clause Groups",
    structuredDomains: "Structured legal domains",
    clause: "Clause",
    legalRelationshipDetected: "Legal relationship detected.",
    contradictionsDetected: "Contradictions Detected",
    other: "Other",
    high: "High",
    medium: "Medium",
    low: "Low",
  },
  fr: {
    highRisk: "Risques élevés",
    mediumRisk: "Risques moyens",
    lowRisk: "Risques faibles",
    contradictions: "Contradictions",
    dependencies: "Dépendances",
    riskHeatmap: "Carte des risques",
    topRisks: "Principaux risques",
    executiveNarrative: "Résumé exécutif",
    dependencyGraph: "Graphe des dépendances",
    legalRelationGraph: "Graphe des relations juridiques",
    clauseGroups: "Groupes de clauses",
    structuredDomains: "Domaines juridiques structurés",
    clause: "Clause",
    legalRelationshipDetected: "Relation juridique détectée.",
    contradictionsDetected: "Contradictions détectées",
    other: "Autres",
    high: "Élevé",
    medium: "Moyen",
    low: "Faible",
  },
  ar: {
    highRisk: "مخاطر مرتفعة",
    mediumRisk: "مخاطر متوسطة",
    lowRisk: "مخاطر منخفضة",
    contradictions: "التناقضات",
    dependencies: "التبعيات",
    riskHeatmap: "خريطة المخاطر",
    topRisks: "أهم المخاطر",
    executiveNarrative: "السرد التنفيذي",
    dependencyGraph: "مخطط التبعيات",
    legalRelationGraph: "مخطط العلاقات القانونية",
    clauseGroups: "مجموعات البنود",
    structuredDomains: "المجالات القانونية المنظمة",
    clause: "بند",
    legalRelationshipDetected: "تم اكتشاف علاقة قانونية.",
    contradictionsDetected: "التناقضات المكتشفة",
    other: "أخرى",
    high: "مرتفع",
    medium: "متوسط",
    low: "منخفض",
  },
};

const GROUP_TRANSLATIONS: any = {
  en: {
    other: "Other",
    performance_service_obligations: "Performance & Service Obligations",
    compensation_payment: "Compensation & Payment",
    confidentiality_data: "Confidentiality & Data",
    ip_ownership_license: "IP Ownership & Licensing",
    dispute_jurisdiction_arbitration: "Disputes & Arbitration",
    liability_indemnity_insurance: "Liability, Indemnity & Insurance",
    termination: "Termination",
    confidentiality: "Confidentiality",
  },
  fr: {
    other: "Autres",
    performance_service_obligations: "Obligations de service et de performance",
    compensation_payment: "Rémunération et paiements",
    confidentiality_data: "Confidentialité et données",
    ip_ownership_license: "Propriété intellectuelle et licences",
    dispute_jurisdiction_arbitration: "Litiges et arbitrage",
    liability_indemnity_insurance: "Responsabilité, indemnisation et assurance",
    termination: "Résiliation",
    confidentiality: "Confidentialité",
  },
  ar: {
    other: "أخرى",
    performance_service_obligations: "التزامات الأداء والخدمات",
    compensation_payment: "التعويضات والمدفوعات",
    confidentiality_data: "السرية والبيانات",
    ip_ownership_license: "الملكية الفكرية والتراخيص",
    dispute_jurisdiction_arbitration: "النزاعات والتحكيم",
    liability_indemnity_insurance: "المسؤولية والتعويض والتأمين",
    termination: "إنهاء العقد",
    confidentiality: "السرية",
  },
};

const RELATION_TRANSLATIONS: any = {
  en: {
    ip_confidentiality:
      "IP rights may depend on confidential information handling.",
    legal_relationship:
      "Legal relationship detected.",
  },
  fr: {
    ip_confidentiality:
      "Les droits de propriété intellectuelle peuvent dépendre du traitement des informations confidentielles.",
    legal_relationship:
      "Relation juridique détectée.",
  },
  ar: {
    ip_confidentiality:
      "قد تعتمد حقوق الملكية الفكرية على كيفية التعامل مع المعلومات السرية.",
    legal_relationship:
      "تم اكتشاف علاقة قانونية.",
  },
};

const uiText = (
  key: string,
  language: string,
) => {
  return (
    DASHBOARD_TRANSLATIONS?.[language]?.[key] ||
    DASHBOARD_TRANSLATIONS?.en?.[key] ||
    key
  );
};

const translateGroupLabel = (
  value: string,
  language: string,
) => {
  const normalized = String(value || "").trim();

  if (normalized === "Document Preamble") {
    return language === "ar"
      ? "مقدمة العقد"
      : language === "fr"
      ? "Préambule du contrat"
      : "Document Preamble";
  }

  return (
    GROUP_TRANSLATIONS?.[language]?.[normalized] ||
    GROUP_TRANSLATIONS?.en?.[normalized] ||
    normalized
  );
};

const translateRelationText = (
  value: string,
  language: string,
) => {
  const normalized = String(value || "").trim();
  const normalizedLower = normalized.toLowerCase();

  if (!normalized) {
    return RELATION_TRANSLATIONS?.[language]?.legal_relationship;
  }

  if (
    normalizedLower.includes("confidentiality breaches") &&
    normalizedLower.includes("liability")
  ) {
    return language === "ar"
      ? "قد تؤثر انتهاكات السرية على المسؤولية أو التزامات التعويض."
      : language === "fr"
      ? "Les violations de confidentialité peuvent affecter la responsabilité ou les obligations d’indemnisation."
      : normalized;
  }

  if (
    normalizedLower.includes("ownership rights") &&
    normalizedLower.includes("confidential")
  ) {
    return language === "ar"
      ? "قد تعتمد حقوق الملكية الفكرية أو حقوق الملكية على كيفية التعامل مع المعلومات السرية."
      : language === "fr"
      ? "Les droits de propriété intellectuelle ou de propriété peuvent dépendre du traitement des informations confidentielles."
      : normalized;
  }

  if (
    normalized ===
    "IP rights may depend on confidential information handling."
  ) {
    return RELATION_TRANSLATIONS?.[language]?.ip_confidentiality;
  }

  if (normalized === "Legal relationship detected.") {
    return RELATION_TRANSLATIONS?.[language]?.legal_relationship;
  }

  return normalized;
};

export default function ExecutiveDashboard({
  result,
  language,
  showGraphs = false,
}: Props) {

  const source =
    result?.clauses || result || {};

  const executive =
    source?.executive_summary || {};

  const overview =
    executive?.risk_overview || {};

  const contradictions =
    source?.contradictions || [];

  const dependencyGraph =
    source?.dependency_graph || {};

  const graphEdges =
    (dependencyGraph?.edges || []).slice(0, 40);

  const legalRelationGraph =
    source?.legal_relation_graph || {};

  const rawClauseGroups =
    source?.clause_groups || [];

  const clauseGroups = Array.isArray(rawClauseGroups)
    ? rawClauseGroups
    : Array.isArray(rawClauseGroups?.groups)
    ? rawClauseGroups.groups
    : Array.isArray(rawClauseGroups?.results)
    ? rawClauseGroups.results
    : Array.isArray(rawClauseGroups?.clause_groups)
    ? rawClauseGroups.clause_groups
    : [];

  const dependencyCount =
    dependencyGraph?.edges?.length ||
    executive?.dependency_summary?.edges_count ||
    source?.dependency_insights?.edges_count ||
    0;

  const narrative =
    source?.executive_risk_narrative || "";

  const topRisks =
    executive?.top_risks || [];

  return (
    <section className="space-y-6">

      <div className="sticky top-4 z-10 backdrop-blur-sm">
        <div className="grid gap-4 md:grid-cols-4">

        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <div className="text-sm text-slate-500">
            {uiText("highRisk", language)}
          </div>

          <div className="mt-2 text-3xl font-bold text-red-600">
            {overview.high || 0}
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <div className="text-sm text-slate-500">
            {uiText("mediumRisk", language)}
          </div>

          <div className="mt-2 text-3xl font-bold text-amber-500">
            {overview.medium || 0}
          </div>
        </div>

        {contradictions.length > 0 && (
          <div className="rounded-2xl border bg-white p-5 shadow-sm">
            <div className="text-sm text-slate-500">
              {uiText("contradictions", language)}
            </div>

            <div className="mt-2 text-3xl font-bold text-violet-600">
              {contradictions.length}
            </div>
          </div>
        )}

        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <div className="text-sm text-slate-500">
            {uiText("dependencies", language)}
          </div>

          <div className="mt-2 text-3xl font-bold text-blue-600">
            {dependencyCount}
          </div>
        </div>
        </div>
      </div>

      <div className="rounded-3xl border bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold">
          {uiText("riskHeatmap", language)}
        </h2>

        <div className="mt-5 space-y-4">
          {[
            [uiText("high", language), overview.high || 0, "bg-red-500"],
            [uiText("medium", language), overview.medium || 0, "bg-amber-500"],
            [uiText("low", language), overview.low || 0, "bg-green-500"],
          ].map(([label, value, color]: any) => {
            const total =
              (overview.high || 0) +
              (overview.medium || 0) +
              (overview.low || 0);

            const percent = total
              ? Math.round((value / total) * 100)
              : 0;

            return (
              <div key={label}>
                <div className="mb-1 flex justify-between text-sm">
                  <span>{label}</span>
                  <span>{percent}%</span>
                </div>

                <div className="h-3 rounded-full bg-slate-100">
                  <div
                    className={`h-3 rounded-full ${color}`}
                    style={{ width: `${percent}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="rounded-3xl border bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold">
          {uiText("topRisks", language)}
        </h2>

        <div className="mt-5 space-y-4">

          {topRisks.map(
            (
              risk: any,
              index: number
            ) => (
              <div
                key={index}
                className="rounded-2xl border p-4"
              >

                <div className="flex items-center justify-between">

                  <div className="font-semibold text-slate-900">
                    {risk.title}
                  </div>

                  <RiskBadge
                    risk={risk.risk_level}
                    language={language}
                  />
                </div>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {risk.legal_insight}
                </p>
              </div>
            )
          )}

        </div>
      </div>

      <div className="rounded-3xl border bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold">
          {uiText("executiveNarrative", language)}
        </h2>

        {narrative && (
          <p className="mt-4 leading-7 text-slate-700 whitespace-pre-wrap">
            {narrative}
          </p>
        )}
      </div>

      {showGraphs && !!dependencyGraph?.edges?.length && (
        <div className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">
            {uiText("dependencyGraph", language)}
          </h2>

        <div className="mt-5 space-y-3">
          {graphEdges.slice(0, 8).map(
            (edge: any, index: number) => {
              const nodes = dependencyGraph?.nodes || [];

              const fromNode = nodes.find(
                (node: any) => node.id === edge.from
              );

              const toNode = nodes.find(
                (node: any) => node.id === edge.to
              );

              return (
                <div
                  key={index}
                  className="rounded-2xl border bg-slate-50 p-4 text-sm"
                >
                  <div className="font-semibold text-slate-900">
                    {fromNode?.title || uiText("clause", language)} → {toNode?.title || uiText("clause", language)}
                  </div>

                  <div className="mt-2 text-slate-600">
                    {translateRelationText(edge.reason, language)}
                  </div>
                </div>
              );
            }
          )}

        </div>
      </div>
      )}

      {showGraphs && !!legalRelationGraph?.edges?.length && (
        <div className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">
            {uiText("legalRelationGraph", language)}
          </h2>

        <div className="mt-5 space-y-3">
          {(legalRelationGraph?.edges || []).slice(0, 8).map(
            (edge: any, index: number) => {
              const nodes = legalRelationGraph?.nodes || [];

              const fromNode = nodes.find(
                (node: any) => node.id === edge.from
              );

              const toNode = nodes.find(
                (node: any) => node.id === edge.to
              );

              return (
                <div
                  key={index}
                  className="rounded-2xl border bg-blue-50 p-4 text-sm"
                >
                  <div className="font-semibold text-slate-900">
                    {fromNode?.title || uiText("clause", language)} → {toNode?.title || uiText("clause", language)}
                  </div>

                  <div className="mt-2 text-slate-600">
                    {translateRelationText(edge.reason || edge.relation_type, language)}
                  </div>
                </div>
              );
            }
          )}

        </div>
      </div>
      )}

      {showGraphs && !!clauseGroups.length && (
        <div className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">
            {uiText("clauseGroups", language)}
          </h2>

          <div className="mt-3 text-xs text-slate-500 uppercase tracking-wide">
            {uiText("structuredDomains", language)}
          </div>

          <div className="mt-5 space-y-4">
          {clauseGroups.slice(0, 8).map(
            (group: any, index: number) => (
              <div
                key={index}
                className="rounded-2xl border bg-slate-50 p-4"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="font-semibold text-slate-900">
                      {translateGroupLabel(group.title || group.group_title || group.name || "other", language)}
                    </div>

                    {group.summary && (
                      <p className="mt-2 text-sm leading-6 text-slate-600">
                        {group.summary}
                      </p>
                    )}
                  </div>

                  {group.risk_level && (
                    <RiskBadge
                      risk={group.risk_level}
                      language={language}
                    />
                  )}
                </div>

                {!!group.clauses?.length && (
                  <div className="mt-4 space-y-2">
                    {group.clauses.slice(0, 6).map(
                      (clause: any, clauseIndex: number) => (
                        <div
                          key={clauseIndex}
                          className="rounded-xl border bg-white px-3 py-2 text-sm text-slate-700"
                        >
                          {translateGroupLabel(
                            clause.title || clause.clause_title || clause,
                            language
                          )}
                        </div>
                      )
                    )}
                  </div>
                )}
              </div>
            )
          )}

        </div>
      </div>
      )}

      {showGraphs && !!contradictions.length && (
        <div className="rounded-3xl border bg-white p-6 shadow-sm">

          <h2 className="text-xl font-semibold">
            {uiText("contradictionsDetected", language)}
          </h2>

          <div className="mt-5 space-y-4">

            {contradictions.map(
              (
                item: any,
                index: number
              ) => (
                <div
                  key={item.id ? `${item.id}-${index}` : index}
                  className="rounded-2xl border border-red-200 bg-red-50 p-4"
                >

                  <div className="flex items-center justify-between gap-3">
                    <div className="font-semibold text-red-700">
                      {item.label || item.id}
                    </div>

                    {item.severity && (
                      <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-semibold uppercase text-red-800">
                        {item.severity}
                      </span>
                    )}
                  </div>

                  <p className="mt-2 text-sm text-red-600">
                    {item.message}
                  </p>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </section>
  );
}