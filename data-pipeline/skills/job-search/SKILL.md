# Job Search

Description: Find, rank, and explain relevant IT job postings using semantic search and structured filters.
Triggers: job, việc làm, tìm việc, tuyển dụng, apply, vị trí, role, công ty, remote, hybrid, onsite, phù hợp

## When to use

Use this skill when the user wants to find jobs, compare job options, identify suitable roles, or ask which postings match their skills/background.

## Workflow

1. Extract user intent:
   - target role/title
   - required skills
   - location
   - level
   - work mode
   - salary expectation
2. Use `semantic_search_tool` for natural-language matching.
3. Use `execute_sql_tool` when the user gives strict filters such as city, salary band, level, or work mode.
4. Rank results by a blend of semantic relevance, salary fit, skill fit, and recency.
5. Explain why each recommendation matches.

## Response format

- Give 3-5 best matches unless the user asks for more.
- For each job include: title, company, location, salary, match reason, and caveat.
- If results are weak, say what constraint caused it and suggest a broader search.

## Guardrails

- Do not claim the user is guaranteed to get a job.
- Do not recommend roles solely by keyword match when semantic fit is poor.
- If salary is hidden, label it clearly and use prediction only when helpful.
