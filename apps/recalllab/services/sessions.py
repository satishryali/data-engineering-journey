"""A saved question plan; dates/stages still belong exclusively to coach.py."""
from dataclasses import replace
from datetime import date
import json
from services.questions import question, daily_queue, ALIASES
from services.records import now
from challenges.catalog import PYTHON, SQL


def varied_question(records, item, day, style, nonce=0):
    q = question(records, item, day, nonce)
    if item.startswith('RLP-'):
        # Published business prompts must not become invented generic note questions.
        return {'question': q.dict(), 'runner': None, 'minutes': 10, 'style': 'coding'}
    concept = ALIASES.get(item,item)
    number = day.toordinal()*10 + nonce
    runner = None
    if style == 'prediction':
        if concept.startswith('sql.'):
            if concept in ('sql.join.preservation','sql.join.keys'):
                prompt = f'Customers IDs: {number}, {number+1}. Orders(order_id,customer_id): (1,{number}), (2,{number}). Predict SELECT c.id,o.order_id FROM customers c LEFT JOIN orders o ON c.id=o.customer_id ORDER BY c.id,o.order_id. Answer as a JSON array of rows, using null for SQL NULL.'
                expected = [[number,1],[number,2],[number+1,None]]
            elif concept == 'sql.sum.nulls':
                prompt = f'Batch {number}: amount values are NULL, {nonce+9}, NULL. Predict [COUNT(*),COUNT(amount),SUM(amount)] as JSON.'
                expected = [3,1,nonce+9]
            else:
                prompt = f'Customer {number} has two matching orders; customer {number+1} has none. After LEFT JOIN, predict [COUNT(*) for first, COUNT(order_id) for first, COUNT(*) for second, COUNT(order_id) for second] as JSON.'
                expected = [2,2,1,0]
            q = replace(q, prompt=prompt, expected=expected, mode='Output prediction', dimension='reading_predicting', solution=json.dumps(expected)+'\nTrace preserved customers and actual matching orders separately.')
        elif concept in ('py.csv.read','py.csv.write'):
            prompt = f'Predict the final output as JSON. Explain types separately.\n```python\nimport csv, io\ntext = \'id,name\\n{number},"Asha, Sales"\\n\'\nrows = list(csv.DictReader(io.StringIO(text)))\nprint([rows[0]["id"], rows[0]["name"], len(rows)])\n```'
            expected = [str(number),'Asha, Sales',1]
            q = replace(q,prompt=prompt,expected=expected,mode='Output prediction',dimension='reading_predicting',solution=json.dumps(expected)+'\nThe header supplies keys; quoted commas stay inside a field; CSV reader values are strings.')
        elif concept == 'py.functions.basics':
            q = replace(q,prompt=f'Predict output as JSON.\n```python\ndef collect(rows):\n    result = []\n    for row in rows:\n        result.append(row["id"])\n    return result\nprint([collect([{{"id": {number}}}]), collect([])])\n```',expected=[[number],[]],mode='Output prediction',dimension='reading_predicting',solution=json.dumps([[number],[]])+'\nEach call creates a fresh local list.')
        elif q.expected is None:
            q = replace(q,mode='Predict and explain',dimension='reading_predicting',prompt=f'For scenario {number}, give a minimal example of {q.title}, predict the result and explain one edge case. Keep to the mapped note section. This needs human assessment.')
    elif style == 'debug':
        if concept.startswith('sql.'):
            broken = 'COUNT(*)' if concept not in ('sql.join.preservation','sql.join.keys') else 'INNER JOIN'
            prompt = f'A report for batch {number} must include a customer with no orders. Its current query uses {broken}. Reconstruct a three-row fixture, show the actual wrong result and correct the query. Explain the difference. Preserve distinct IDs even when names match.'
        elif concept.startswith('py.csv.'):
            prompt = f'Batch {number}: a DictWriter has fieldnames=["id","name"] but receives {{"id":{number},"label":"Asha"}}. Predict the failure, identify the mismatch and show a corrected scratch example including a read-back check. Do not alter project files.'
        elif concept.startswith('py.dict.'):
            prompt = f'Batch {number}: d={{"id":{number}}}; code evaluates d["amount"] even though amount may be absent. Explain the observed exception, give an appropriate lookup/default approach and show both present/missing input behavior. Preserve d.'
        else:
            prompt = f'For {q.title}, construct a small failing example for batch {number}, show expected versus actual behavior, identify the cause and make the smallest correction. Include a changed-input check. Use only the mapped source material.'
        q = replace(q,prompt=prompt,expected=None,mode='Debugging reconstruction',dimension='debugging',solution='Compare the actual failure and correction with the cited section. A human review of output and reasoning is required.')
    elif style == 'explain':
        q = replace(q,prompt=f'Explain {q.title} using a tiny batch numbered {number}. State why it is useful, give one input/output example, and explain an edge case without opening notes. Your explanation is assessed separately from previous code/output tests.',expected=None,mode='Short-answer recall',dimension='explaining',solution='Review the mapped section after attempting. Check that your explanation includes purpose, input/output and a concrete edge case.')
    elif style == 'coding':
        sql_kind = 'join' if concept in ('sql.join.preservation','sql.join.keys') else 'sum' if concept=='sql.sum.nulls' else 'count'
        if concept.startswith('sql.'):
            challenge = next(c for c in SQL if c[4]==sql_kind)
            q = replace(q,prompt=f'{challenge[3]}\n\nSchemas: customers(customer_id INTEGER,name TEXT); orders(order_id INTEGER,customer_id INTEGER,amount INTEGER). Sample customers: (1,Asha),(2,Asha),(3,Devi). Orders: (101,1,7),(102,1,NULL),(103,3,0). Run Query validates three controlled fixtures. Task variation {number}.',expected=None,mode='SQL coding',dimension='building',solution='Compare each fixture output; do not infer explanation proficiency from a passing query.')
            runner = sql_kind
        else:
            challenge = next((c for c in PYTHON if c[1]==concept), None)
            q = replace(q,prompt=(challenge[3] if challenge else q.prompt)+f'\n\nUse fresh scratch inputs with identifier {number}. Submit code plus verification output for human assessment. Python execution is disabled until a verified isolated runner is configured.',expected=None,mode='Python coding' if concept.startswith('py.') else 'Practical application',dimension='building',solution='A human reviewer must verify code behavior and edge cases; source is never executed by RecallLab.')
    q = replace(q,variant_id=q.variant_id+'-'+style)
    return {'question':q.dict(), 'runner':runner, 'minutes':10 if style=='coding' else 5, 'style':style}


def get_plan(records, journal, session, minutes=20, day=None, max_items=None):
    # A limit bounds new work; saved tasks and submitted evidence are never removed.
    max_items = max(1, int(max_items)) if max_items is not None else None
    key = 'plan:'+session
    existing = journal.get('settings', key)
    if existing:
        if minutes > existing['budget_minutes']:
            used = {e.get('task_variant') for e in records.events()+journal.attempts()}
            used.update(t['question']['variant_id'] for t in existing['tasks'])
            while sum(t['minutes'] for t in existing['tasks'])+5 <= minutes and (max_items is None or len(existing['tasks']) < max_items):
                i = len(existing['tasks'])
                style = ['prediction','debug','explain'][i%3]
                item = existing['tasks'][i%len(existing['tasks'])]['question']['item_id']
                nonce = i
                task = varied_question(records,item,date.fromisoformat(existing['date_ist']),style,nonce)
                while task['question']['variant_id'] in used:
                    nonce += 1
                    task = varied_question(records,item,date.fromisoformat(existing['date_ist']),style,nonce)
                used.add(task['question']['variant_id']); existing['tasks'].append(task)
            existing['budget_minutes'] = minutes
            journal.put('settings',key,existing)
        return existing
    day = day or now().date()
    targets = daily_queue(records, minutes, day)
    used = {e.get('task_variant') for e in records.events()+journal.attempts()}
    styles = ['prediction','coding','explain'] if day.toordinal()%2==0 else ['debug','coding','prediction']
    if minutes > 20:
        styles += ['explain' if styles[0]=='debug' else 'debug']
    tasks, remaining = [], minutes
    for i, style in enumerate(styles):
        if max_items is not None and len(tasks) >= max_items:
            break
        if not targets:
            break
        cost = 10 if style=='coding' else 5
        if remaining < cost:
            continue
        target = targets[min(i//2,len(targets)-1)]
        nonce = i
        task = varied_question(records,target['id'],day,style,nonce)
        while task['question']['variant_id'] in used:
            nonce += 1
            task = varied_question(records,target['id'],day,style,nonce)
        used.add(task['question']['variant_id'])
        tasks.append(task)
        remaining -= cost
    if not tasks:
        # A deliberate initial diagnostic if no due/ready target is proposed.
        topics = records.json('tracking/topic-map.json')['topics']
        ready = next((t for t in topics if not t['prerequisites']), topics[0])
        tasks.append(varied_question(records,ready['id'],day,'prediction'))
    planned_minutes = sum(t['minutes'] for t in tasks)
    plan = {'session_id':session,'date_ist':str(day),'budget_minutes':planned_minutes,'targets':targets,'tasks':tasks}
    journal.put('settings',key,plan)
    if minutes > planned_minutes:
        return get_plan(records,journal,session,minutes,day,max_items)
    return plan
