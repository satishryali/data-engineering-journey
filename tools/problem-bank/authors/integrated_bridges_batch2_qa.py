"""Read-only QA for the explicit JOBBR-081..239 batch and current bank."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT / 'tools/problem-bank'
sys.path.insert(0, str(ROOT / 'apps/recalllab'))
sys.path.insert(0, str(ROOT / 'tools'))
from services.curriculum import load_curriculum  # noqa: E402
from services.bank_validation import audit  # noqa: E402
from publish_problem_bank import stage_snapshot  # noqa: E402
from integrated_bridges_batch2 import make  # noqa: E402


def main():
    path = BANK / 'integrated-bridges-batch2.json'
    rows = json.loads(path.read_text(encoding='utf-8'))
    assert rows == make(), 'File differs from frozen authored contracts'
    assert len(rows) == 159
    assert [r['id'] for r in rows] == [f'RLP-JOBBR-{i:03d}' for i in range(81, 240)]
    assert Counter(r['level'] for r in rows) == {0:8,1:12,2:14,3:16,4:17,5:17,6:17,7:17,8:15,9:14,10:12}
    for left, right in zip(rows, rows[1:]):
        assert right['level'] in (left['level'], left['level'] + 1)
        assert left['id'] in right['prerequisites']
    data = load_curriculum(ROOT)
    present = {p['id']:p for p in data['problems']}
    old = json.loads((BANK / 'integrated-bridges.json').read_text(encoding='utf-8'))
    assert [p['id'] for p in old] == [f'RLP-JOBBR-{i:03d}' for i in range(1, 81)]
    for row in rows:
        if row['id'] in present:
            assert row == present[row['id']], 'Published ID has different content'
        else:
            present[row['id']] = row
    proposed = dict(data, problems=list(present.values()),
                    technologies=json.loads(json.dumps(data['technologies'])))
    stage_snapshot(proposed)
    report = audit(proposed)
    assert not report['missing_fields'], report['missing_fields'][:3]
    assert not report['duplicates'], report['duplicates'][:3]
    assert not report['similar_task_candidates'], report['similar_task_candidates'][:3]
    assert not report['broken_prerequisites_and_structure'], report['broken_prerequisites_and_structure'][:3]
    assert not report['job_ready_pathway_errors'], report['job_ready_pathway_errors'][:3]
    assert report['schema_valid']
    print(json.dumps({
        'authored_count': len(rows),
        'id_span': [rows[0]['id'], rows[-1]['id']],
        'levels': dict(sorted(Counter(r['level'] for r in rows).items())),
        'published_bank_before': len(data['problems']),
        'combined_bank_after': len(present),
        'combined_integrated_track': report['technology_counts']['integrated-pipelines'],
        'missing_fields': len(report['missing_fields']),
        'duplicate_contracts_or_ids': len(report['duplicates']),
        'same_task_candidates': len(report['similar_task_candidates']),
        'broken_prerequisites_and_structure': len(report['broken_prerequisites_and_structure']),
        'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'author_sha256': hashlib.sha256((BANK / 'authors/integrated_bridges_batch2.py').read_bytes()).hexdigest(),
    }, indent=2))


if __name__ == '__main__':
    main()
