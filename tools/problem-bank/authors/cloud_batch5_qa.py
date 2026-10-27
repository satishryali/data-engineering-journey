"""Audit unregistered cloud batches against the current published curriculum."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/recalllab'))
from services.curriculum import load_curriculum, validate_curriculum
from services.bank_validation import audit

def check(paths):
    data = load_curriculum(ROOT)
    existing = {p['id'] for p in data['problems']}
    for path in paths:
        records = json.loads(path.read_text(encoding='utf-8'))
        assert isinstance(records, list) and records
        assert len({p['id'] for p in records}) == len(records)
        if existing.intersection(p['id'] for p in records):
            assert {p['id'] for p in records} <= existing, (path, 'partially registered file')
            by_id = {p['id']: p for p in data['problems']}
            assert all(by_id[p['id']] == p for p in records), (path, 'registered content differs')
        else:
            data['problems'].extend(records)
            existing.update(p['id'] for p in records)
        print(path.name, len(records), hashlib.sha256(path.read_bytes()).hexdigest())
    counts = Counter(p['tool_id'] for p in data['problems'])
    for tech in data['technologies']:
        tech['published_total'] = counts[tech['id']]
        for stage in tech['stages']:
            ids = [p['id'] for p in data['problems'] if p['tool_id'] == tech['id'] and p['level'] == stage['level']]
            stage.update(published_problem_ids=ids, status='published' if ids else 'planned')
    issues = audit(data)
    print('total', len(data['problems']), 'counts', {k:v for k,v in issues['technology_counts'].items() if k in ('pyspark','adf','databricks')})
    print('missing',len(issues['missing_fields']),'duplicates',len(issues['duplicates']),
          'near_duplicates',len(issues['similar_task_candidates']),
          'broken',len(issues['broken_prerequisites_and_structure']))
    for key in ('missing_fields','duplicates','broken_prerequisites_and_structure'):
        if issues[key]:print(key,issues[key][:10])
    return 0 if issues['schema_valid'] else 1

if __name__=='__main__':
    sys.exit(check([Path(arg).resolve() for arg in sys.argv[1:]]))
