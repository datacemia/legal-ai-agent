def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_recommendation_prompt(
    analysis_result: dict,
    output_language: str = "en",
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Create ranked business recommendations from the analysis result.

LANGUAGE RULES:
- Output all user-facing text in {language_name}.
- Keep JSON keys in English.
- Return only valid JSON.
- Do not write anything outside JSON.
- Mixed-language explanatory output is forbidden.
- Keep company names, product names, dates, amounts, currencies, and source column names unchanged when appropriate.

GLOBAL DATA-SAFETY RULES:
- Work for any business domain worldwide: SaaS, ecommerce, agencies, restaurants, marketplaces, retail, services, finance operations, logistics, education, healthcare operations, public-sector operations, and general businesses.
- The input data may be in English, French, Arabic, Spanish, or another language.
- Understand multilingual business fields when possible, but do not invent missing values.
- Recommendations must be based only on verified metrics present in the analysis result.
- Never assume that missing values are zero.
- Never treat unavailable revenue, expenses, profit, growth, cashflow, churn, ROAS, CAC, customers, MRR, ARR, AOV, LTV, or forecast values as real metrics.
- Never create recommendations based on unavailable metrics.
- Never invent trends, forecasts, profitability, churn, ROAS, CAC, customer retention, or cashflow issues when the analysis result does not support them.
- If a metric is unavailable, clearly state that it is unavailable instead of using it as evidence.
- Prefer fewer accurate recommendations over many unsupported recommendations.

NON-PERFORMANCE DATASET RULES:
- Product catalogs, inventory lists, SKU lists, price lists, customer reviews, survey comments, reference tables, lookup tables, user lists, content lists, transaction IDs without amounts, and similar non-performance datasets must not generate financial, growth, profitability, cashflow, churn, ROAS, CAC, or forecast recommendations.
- Customer review datasets may support recommendations about collecting structured performance data or connecting review sentiment to future business KPIs, but must not produce revenue, profit, margin, growth, cashflow, churn, ROAS, CAC, or forecast claims unless those metrics are explicitly present.
- Product catalog or inventory datasets may support recommendations about adding business performance fields, but must not claim revenue, profit, growth, stockout risk, margin pressure, or pricing performance unless the analysis result includes verified supporting metrics.
- If analysis_available is false, recommendations must only focus on data readiness, measurement quality, and what data to collect next.
- If the uploaded file does not contain business performance data, recommendations must focus only on data collection and measurement readiness.
- When business performance data is unavailable, recommend collecting dated Revenue, Expenses, Profit, Cashflow, Customer, Orders, Marketing Spend, or Channel data before making executive decisions.

RECOMMENDATION RULES:
- Rank by expected business impact.
- Use only issues supported by the data.
- Avoid generic advice unless the dataset is non-performance; in that case, data-readiness recommendations are appropriate.
- Include clear action steps.
- Do not invent unsupported metrics.
- Use only verified backend KPIs.
- Never invent a Business Health Score.
- Never display None, null, Unknown, N/A, or 0 as a valid score.
- If business_health_score is unavailable, state that it could not be calculated due to insufficient business performance data.
- If revenue, profit, margin, growth, churn, ROAS, CAC, customers, MRR, ARR, AOV, forecast, or cashflow are unavailable, clearly state they are unavailable.
- If recommendations mention a KPI, that KPI must be available and supported in the analysis result.
- Do not recommend scaling acquisition unless acquisition, channel, CAC, ROAS, or conversion data is available.
- Do not recommend reducing churn unless churn, retention, customers, subscriptions, cancellations, or repeat-purchase data is available.
- Do not recommend improving profit margin unless revenue and expense/cost/profit data is available.
- Do not recommend cashflow actions unless cashflow, payment, receivable, payable, or dated financial data is available.
- Do not recommend forecasts unless forecast.available is true and enough dated historical data exists.
- Do not mention backend, backend-calculated, deterministic backend, internal engine, server, database, API, or system architecture in user-facing text.
- Use "verified business metrics" instead of "backend-calculated metrics".
- Use "Business Health Score" instead of technical score wording.

OUTPUT CONTENT RULES:
- For a normal performance dataset, produce practical ranked recommendations based on verified KPIs, risks, opportunities, and data quality.
- For a non-performance dataset, produce only data-readiness recommendations such as:
  - Add dated revenue and order data.
  - Add expenses, cost, or profit fields.
  - Add customer counts, new customers, churned customers, or retention fields.
  - Add marketing spend, channel, CAC, ROAS, or conversion fields.
  - Add cashflow, payment, receivable, or payable fields.
  - Connect review, catalog, or inventory data to verified business performance data before using it for executive decisions.
- Avoid using words like "increase revenue", "improve margin", "reduce churn", or "scale marketing" unless the related metric is actually available.

Return EXACT JSON:

{{
  "recommendations": [
    {{
      "title": "",
      "priority": "low | medium | high",
      "expected_impact": "",
      "action_steps": []
    }}
  ],
  "quick_wins": [],
  "strategic_actions": [],
  "avoid_doing": []
}}

Analysis result:
{analysis_result}
"""
