# Preserved notes-revision history — migration 15 October 2026

`notes-revision-topics.json`, `notes-revision-reviews.jsonl` and
`notes-revision-README.md` are byte-for-byte snapshots from before five-role setup.
Treat the old instructions as historical specification, not active execution rules.
In particular, their save-after-every-answer and begin-diagnostic commands are superseded
by the shared checkpoint-boundary workflow. No learner answer occurred during migration.

The original ten concept IDs, source paths/hashes, nulls, prerequisites, timestamps and
pending `diagnostic-dict-001` remain here. The original reviews file is empty; therefore
no history rows or learning scores were invented during migration. The original five
CSV exercise rows retain every field/date/evidence value. New concept rows are unassessed.

The active concept identity/source registry is `../topic-map.json`. Associations:

| Stable concept ID | Existing broad exercise IDs |
| --- | --- |
| py.dict.access | PY-001, PY-002 |
| py.dict.mutate | PY-001, PY-002 |
| py.context.resources | No matching assessed exercise; concept-only row |
| pg.cursor.results | No matching assessed exercise; concept-only row |
| py.logging.basics | No matching assessed exercise; concept-only row |
| py.paths.imports | No matching assessed exercise; concept-only row |
| py.modules.main | No matching assessed exercise; concept-only row |
| vault.kv.read | No matching assessed exercise; concept-only row |
| py.logging.shared | No matching assessed exercise; concept-only row |
| de.ingest.seeds | No matching assessed exercise; concept-only row |
| sql.join.preservation | SQL-001 |
| sql.count.nulls | SQL-002 |
| sql.join.keys | SQL-001, SQL-002 |
| sql.group.grain | SQL-002 |
| sql.sum.nulls | SQL-003 |
| py.records.cleaning | PY-001 |

The final six IDs identify concepts already present in saved exercise evidence; they are
not new assessed lessons. Associations are many-to-many links, not aliases. In particular,
PY-001 needs guidance while its linked notes concepts remain unassessed; preserve both
facts rather than invent per-concept assessment results.

`diagnostic-dict-001` asked for a dictionary fallback lookup. The learner later explicitly
requested the simpler PY-002 read/update/print task. The newer checkpoint controls the
next session; the old prompt is deferred, unanswered, not failed/completed/deleted.

Source references now use checkout-relative `Notes/...` paths. Prior source hashes are
retained in source_history when byte hashes changed during vault migration/formatting
or targeted note corrections. A changed source does not erase valid review history.
