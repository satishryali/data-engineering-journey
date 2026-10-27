"""Audit the prepared Spark batches before the parent registers them."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/recalllab'))
from services.bank_validation import audit
from services.curriculum import load_curriculum


def main():
    data = deepcopy(load_curriculum(ROOT))
    additions = []
    checksums = {}
    checkpoint = json.loads((ROOT / 'tools/problem-bank/authors/pyspark-batches-9-11-checkpoint.json').read_text(encoding='utf-8'))
    for number in (9, 10, 11):
        path = ROOT / f'tools/problem-bank/pyspark-batch{number}.json'
        payload = path.read_bytes()
        checksums[number] = hashlib.sha256(payload).hexdigest()
        expected = checkpoint['files_sha256'][str(number)]
        assert checksums[number] == expected, (number, 'checksum changed')
        additions += json.loads(payload)
    data['problems'] += additions
    for technology in data['technologies']:
        technology['published_total'] = sum(p['tool_id'] == technology['id'] for p in data['problems'])
    result = audit(data)
    titles = [p['title'].casefold() for p in data['problems'] if p['tool_id'] == 'pyspark']
    duplicate_titles = [title for title, count in Counter(titles).items() if count > 1]
    spark = [p for p in data['problems'] if p['tool_id'] == 'pyspark']
    print(json.dumps({
        'prepared_spark_total': len(spark), 'prepared_total': result['published_total'],
        'new_spark_batch_counts': [sum(p['authoring_batch'] == f'cloud-explicit-{n:03}' for p in additions) for n in (9, 10, 11)],
        'spark_levels': dict(sorted(Counter(p['level'] for p in spark).items())),
        'missing_fields': result['missing_fields'], 'duplicates': result['duplicates'],
        'duplicate_spark_titles': duplicate_titles,
        'similar_task_candidates': result['similar_task_candidates'],
        'broken_prerequisites_and_structure': result['broken_prerequisites_and_structure'],
        'job_ready_pathway_errors': result['job_ready_pathway_errors'],
        'checksums': checksums,
    }, indent=2))
    return 0 if result['schema_valid'] and not duplicate_titles and len(spark) == 400 else 1


if __name__ == '__main__':
    raise SystemExit(main())
