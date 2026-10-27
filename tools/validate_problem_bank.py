"""Audit actual published RecallLab problems and persist a resumable inventory.

Run from any directory: python tools/validate_problem_bank.py --write
Use --require-target for a nonzero exit until all allocation targets are met.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps/recalllab'))
from services.curriculum import load_curriculum
from services.bank_validation import audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--require-target', action='store_true')
    args=parser.parse_args()
    report=audit(load_curriculum(ROOT))
    if args.write:
        destination=ROOT/'tools/problem-bank/manifest.json'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({key:report[key] for key in ('published_total','target_total','technology_counts','remaining_target_problems','schema_valid','quantity_complete')},indent=2))
    print('Missing fields:',len(report['missing_fields']),'Duplicates:',len(report['duplicates']),
          'Similar task groups requiring inspection:',len(report['similar_task_candidates']),
          'Broken prerequisites/structure:',len(report['broken_prerequisites_and_structure']))
    return 0 if report['schema_valid'] and (not args.require_target or report['quantity_complete']) else 1


if __name__=='__main__': sys.exit(main())
