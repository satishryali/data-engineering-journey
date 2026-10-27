"""Offline variations grounded in mapped source sections; no generated mastery."""
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from services.records import now


@dataclass
class Question:
    variant_id: str
    item_id: str
    title: str
    mode: str
    prompt: str
    expected: object
    hints: list
    solution: str
    sources: list
    dimension: str

    def dict(self):
        return asdict(self)


ALIASES = {'PY-001': 'py.records.cleaning', 'PY-002': 'py.dict.access',
           'SQL-001': 'sql.join.preservation', 'SQL-002': 'sql.count.nulls', 'SQL-003': 'sql.sum.nulls'}


def question(records, item_id, day=None, retry=0):
    day = day or now().date()
    if item_id.startswith('RLP-'):
        from services.curriculum import get_problem, learner_prompt
        problem = get_problem(item_id)
        if not problem:
            raise ValueError('Published problem is unavailable; preserve its saved evidence.')
        prompt = ('Reconstruct this business result on changed input and state all help used. '
                  'Use Tools for the problem submission and verified completion counter.\n\n'
                  + json.dumps(learner_prompt(problem), ensure_ascii=False, indent=2))
        return Question(f'Q-{item_id}-{day}-{retry}', item_id, problem['title'],
                        'Practical application', prompt, None, [],
                        'Compare your actual output with every acceptance criterion after attempting. '
                        'Use Tools to review artifacts; no solution is revealed here.', [], 'building')
    topics = {t['id']: t for t in records.json('tracking/topic-map.json')['topics']}
    concept = ALIASES.get(item_id, item_id)
    topic = topics[concept]
    seed = int(hashlib.sha256(f'{item_id}:{day}:{retry}'.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    # Day offset guarantees adjacent-day input variation instead of relying on chance.
    n = day.toordinal() * 10 + retry
    amount = rng.randint(20, 900)
    name = rng.choice(['Kiran', 'Asha', 'Mira', 'Ravi'])
    mode, expected, dimension = 'Explain / apply', None, 'explaining'
    hints = ['Start with one record. Trace each operation before generalising.',
             'Review the mapped section after your attempt, then try a changed example.']
    solution = 'Compare your reasoning with the cited note section. This question needs a tutor assessment; no automatic score is assigned.'
    if concept in ('py.dict.access', 'py.dict.mutate', 'py.dict.remove'):
        mode, dimension = 'Output prediction', 'reading_predicting'
        prompt = (f'Predict the printed output as a JSON array, then explain your reasoning in the explanation box.\n\n'
                  f'```python\nrecord = {{"id": {n}, "amount": "{amount}"}}\n'
                  f'old = record.get("missing", "none")\nrecord["amount"] = "{amount+7}"\n'
                  'print([record["id"], record["amount"], old])\n```')
        expected = [n, str(amount + 7), 'none']
        hints = ['Track the value and type stored under each key.', 'get() can provide a default for an absent key.']
        solution = json.dumps(expected) + '\nAssignment changes the amount value; get returns its default for the absent key.'
        if concept == 'py.dict.remove':
            prompt = f'Predict output as JSON.\n```python\nd = {{"id": {n}, "tag": "new"}}\nx = d.pop("tag")\ny = d.pop("absent", None)\nprint([x, y, len(d)])\n```'
            expected = ['new', None, 1]
            solution = json.dumps(expected) + '\npop removes and returns an existing value; the second pop uses its default.'
    elif concept == 'py.list.records':
        mode, dimension = 'Output prediction', 'reading_predicting'
        prompt = f'Predict output as JSON and explain the filter and dictionary lookup.\n```python\nrows = [{{"id": {n}, "active": True}}, {{"id": {n+1}, "active": False}}]\nselected = []\nfor row in rows:\n    if row["active"]:\n        selected.append(row["id"])\nprint(selected)\n```'
        expected = [n]
        solution = json.dumps(expected) + '\nOnly the active record contributes its ID; the original record dictionaries remain unchanged.'
    elif concept.startswith('py.list.'):
        mode, dimension = 'Output prediction', 'reading_predicting'
        prompt = f'Predict the output as JSON; explain append and indexing.\n```python\nitems = [{n}, {n+1}, {n}]\nitems[1] = {amount}\nitems.append({n+2})\nprint([items[1], len(items), items.count({n})])\n```'
        expected = [amount, 4, 2]
        solution = json.dumps(expected) + '\nReplacing changes one position; append adds one item; repeated values remain.'
    elif concept.startswith('sql.'):
        mode, dimension = 'Query reconstruction', 'building'
        prompt = (f'Customers(customer_id, name): ({n}, "{name}"), ({n+1}, "{name}"), ({n+2}, "Devi").\n\n'
                  f'Orders(order_id, customer_id, amount): (1,{n},20), (2,{n},NULL), (3,{n+2},0).\n\n'
                  'Write a query returning every customer ID, name, actual order count and amount total. '
                  'Keep customers with no orders separate even when names match. Predict the rows, then explain COUNT(*) versus COUNT(order_id) and the unmatched SUM. '
                  'This is manual reconstruction; use Coding Challenges for controlled SQLite output tests.')
        hints = ['Decide which table contains every entity the report must preserve.',
                 'Compare a matched order with NULL amount to a customer with no order.']
    elif concept == 'py.records.cleaning':
        mode, dimension = 'Coding reconstruction', 'building'
        prompt = (f'Write clean_orders(rows) for [{{"id": {n}, "amount": " {amount} "}}, '
                  f'{{"id": {n+1}, "amount": "bad"}}, {{"id": {n+2}, "amount": "0"}}]. '
                  'Return valid copied records with integer amounts and rejected originals with reasons. '
                  'Preserve input. Include checks for repeated calls and empty input. Submit code, predicted output, and your verification. Execution is manual.')
    elif concept == 'py.functions.basics':
        mode, dimension = 'Debug and reconstruct', 'debugging'
        prompt = (f'```python\nresults = []\ndef collect(rows):\n    for row in rows:\n        results.append(row["id"])\n    return results\n```\n'
                  f'Predict collect([{{"id": {n}}}]) then collect([]). Explain the repeated-call problem and reconstruct a function with a fresh result on each call.')
    elif concept in ('py.csv.read', 'py.csv.write'):
        mode, dimension = 'Coding reconstruction', 'building'
        prompt = (f'In a scratch file, work with two records: {{"id": {n}, "name": "{name}, Sales"}} and {{"id": {n+1}, "name": "Devi"}}. '
                  'Write a CSV with id,name headers, then read it back as dictionaries. Show expected values/types, explain column order, commas in names and newline handling. '
                  'Do not change your project files. Execution is manual.')
    elif concept in ('py.files.methods', 'py.context.resources'):
        mode, dimension = 'Explain and debug', 'debugging'
        prompt = (f'A scratch file contains "batch-{n}\\n{amount}\\n". Compare read(), readline(), and readlines() after reopening the file each time. '
                  'Explain what a second read() on the same handle returns, where seek(0) fits, and what with does when an exception occurs. Include expected outputs.')
    elif concept in ('py.random.basics', 'py.faker.basics'):
        mode = 'Realistic application'
        prompt = (f'You need {n % 100 + 5} synthetic records for a repeatable test, with distinct IDs and amounts from {amount} to {amount+50}. '
                  'Describe and code the generation. Explain what a seed does and does not guarantee, and how you would verify bounds and uniqueness. '
                  'Use the studied random/Faker tools only where useful; do not modify RDS-001.')
    else:
        section = topic.get('note_sections', [{}])[retry % max(1, len(topic.get('note_sections', [])))]
        prompt = (f'Without opening notes, explain {topic["name"]} for a small batch numbered {n}. '
                  f'Give a minimal example, predict its output, identify one failure and explain how to diagnose it. '
                  f'Focus on the mapped section: {section.get("key", topic["name"])}. '
                  'This is an initial diagnostic if you have not previously been assessed; unfamiliar is not failed.')
    return Question(f'Q-{item_id}-{day}-{retry}', item_id, topic['name'], mode, prompt, expected,
                    hints, solution, topic.get('note_sections') or [dict(path=s['path'], key='Source evidence; explanation note not yet mapped') for s in topic.get('sources', [])], dimension)


def daily_queue(records, minutes=20, day=None):
    state, _ = records.coverage(day)
    from services.records import load_coach
    return load_coach(records.root).note_revision.selection(state, records.csv('revision-queue.csv'), minutes)


def evaluate(q, answer, help_used=None, notes_used=False, hints=0):
    if not answer.strip():
        raise ValueError('Write an answer before submitting.')
    if q.expected is None:
        return {'score': None, 'result': 'assisted' if help_used or notes_used or hints else 'unknown',
                'feedback': 'Saved for manual tutor review. No correctness or proficiency score assigned.', 'evaluation': 'manual_pending', 'correct': None}
    try:
        correct = json.dumps(json.loads(answer), sort_keys=True) == json.dumps(q.expected, sort_keys=True)
    except (ValueError, TypeError):
        correct = False
    assisted = bool(help_used or notes_used or hints)
    independent = help_used is False and not notes_used and hints == 0
    return {'score': (3 if independent else 1 if assisted else None) if correct else 0,
            'result': ('independent' if independent else 'assisted' if assisted else 'unknown') if correct else 'needs_guidance',
            'feedback': 'Output matches the reference. Explanation is not automatically assessed.' if correct else 'Output differs from the reference; trace values and types. Try a changed example after feedback.',
            'evaluation': 'exact_output', 'correct': correct}
