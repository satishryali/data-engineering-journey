# Weekly learning summaries

Generate a concise evidence-based summary on request or at the first session after a
week ends. Use `python tracking/coach.py weekly --week YYYY-MM-DD --as-of YYYY-MM-DD`,
where the first date is Monday in IST. No background job runs.

Reports are generated views of the daily history, actual reviews, mistake observations,
dimension-specific skill evidence and existing study log. Label partial weeks and later
reconstruction. Compare actual evidence of independence, not time spent or roadmap dates.
Keep unassessed areas and a manageable next focus explicit. Never invent study on missing
days. Current mistake status is read from the canonical tracker; past recurrence counts
use only observations through that report's as-of date.
