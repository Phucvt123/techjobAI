# Market Insight

Description: Explain IT hiring trends, hot skills, location demand, and market movements from warehouse aggregates.
Triggers: market, thị trường, xu hướng, trend, hot skill, kỹ năng hot, demand, nhu cầu, insight, dashboard, analytics

## When to use

Use this skill when the user asks about market trends, top skills, hiring demand by location, salary movement, or dashboard-style analysis.

## Workflow

1. Determine the analysis dimension:
   - skill demand
   - salary trend
   - location demand
   - monthly hiring trend
   - company/role distribution
2. Query aggregate or mart tables first:
   - `warehouse_marts.mart_skill_demand`
   - `warehouse_marts.mart_location_demand`
   - `warehouse_warehouse.agg_top_skills`
   - `warehouse_warehouse.agg_trend_monthly`
   - `warehouse_warehouse.dashboard_cache`
3. Use `generate_chart_tool` when comparing multiple categories or months.
4. Translate raw numbers into practical interpretation for candidates or recruiters.

## Response format

- Start with the top insight in one sentence.
- Then provide supporting metrics.
- Add implications: what candidates should learn, what recruiters should watch, or what roles are becoming more competitive.

## Guardrails

- Do not overstate causality from descriptive aggregates.
- Mention time range if the data/table exposes it.
- If aggregate data is stale or missing, say the insight is limited.
