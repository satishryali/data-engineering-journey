"""Read-only interview question selector. Assessment records use coach.py."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ('sql', 'python', 'pyspark', 'adf', 'adls', 'databricks', 'delta_incremental',
              'modelling', 'airflow', 'dbt', 'docker', 'git_cicd', 'security_monitoring',
              'incidents', 'architecture', 'experience')
FIELDS = {'id', 'category', 'difficulty', 'prerequisites', 'minutes', 'scenario',
          'task', 'sample_input', 'expected_output', 'sources', 'item_id'}


def load(root=ROOT):
    bank = json.loads((root / 'tracking/interview/questions.json').read_text(encoding='utf-8'))
    seen = set()
    for q in bank['questions']:
        if set(q) != FIELDS or q['id'] in seen:
            raise ValueError('Invalid/duplicate question fields; answers do not belong in the prompt bank')
        seen.add(q['id'])
        if q['category'] not in CATEGORIES or q['difficulty'] not in ('foundation', 'intermediate', 'advanced'):
            raise ValueError('Unknown category or difficulty')
        if not all(q[k] for k in ('task', 'scenario', 'sources', 'prerequisites', 'sample_input', 'expected_output')):
            raise ValueError('Incomplete question')
        if type(q['minutes']) is not int or q['minutes'] <= 0 or not all(s.startswith('https://') for s in q['sources']):
            raise ValueError('Invalid time or source reference')
    if set(CATEGORIES) != {q['category'] for q in bank['questions']}:
        raise ValueError('Missing assessment category')
    return bank['questions']


def present(questions, ident):
    q = next((q for q in questions if q['id'] == ident), None)
    if q is None:
        raise ValueError('Unknown question ID')
    # Whitelist learner-facing prompt fields, even if the storage format later grows.
    return {k: q[k] for k in ('id', 'category', 'difficulty', 'minutes', 'scenario', 'task', 'sample_input', 'expected_output')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'question', 'list'))
    parser.add_argument('--id')
    args = parser.parse_args()
    try:
        questions = load()
        if args.command == 'validate':
            print(f'Validated {len(questions)} questions across {len(CATEGORIES)} categories; no answers or results stored.')
        elif args.command == 'list':
            print('\n'.join(f'{q["id"]}: {q["category"]} ({q["difficulty"]})' for q in questions))
        else:
            print(json.dumps(present(questions, args.id), indent=2))
    except (ValueError, KeyError) as error:
        parser.exit(1, f'{error}\n')
