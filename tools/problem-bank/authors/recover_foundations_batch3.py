"""Recover authored third-round rows after interrupted agent authoring.

Unreadable compact prose stays draft. Earlier published files are untouched.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT / 'tools/problem-bank'
sys.path.insert(0, str(Path(__file__).resolve().parent))
from foundations_batch3 import ROWS
from foundations_batch2 import vocabulary, make_readable

DOCS = {
    'python': ['https://docs.python.org/3/library/urllib.request.html',
               'https://docs.python.org/3/library/csv.html'],
    'sql': ['https://www.postgresql.org/docs/current/queries.html'],
}

def build(tool, rows):
    base = json.loads((ROOT/'tools/curriculum.json').read_text(encoding='utf-8'))
    existing = [p for p in base['problems'] if p['tool_id'] == tool]
    for suffix in ('', '-batch2'):
        existing += json.loads((BANK/f'{tool}{suffix}.json').read_text(encoding='utf-8'))
    number = max(int(p['id'].rsplit('-', 1)[1]) for p in existing) + 1
    prefix = 'PY' if tool == 'python' else 'SQL'
    readable = make_readable(vocabulary())
    latest = {level: max((p for p in existing if p['level'] == level), key=lambda p:p['id'])
              for level in range(11) if any(p['level'] == level for p in existing)}
    result, previous = [], None
    for level,title,task,fixture,expected,boundary in rows:
        def cleaned(value):
            value = readable(value)
            for before, after in (
                ('net work','network'), ('end point','endpoint'),
                ('Aonly','A only'), ('Bonly','B only'),
                ('Aunits2','A units 2'), ('Bunits2','B units 2')):
                value = value.replace(before, after)
            return value
        title,task,fixture,expected,boundary = [cleaned(value) for value in
            (title,task,fixture,expected,boundary)]
        ident = f'RLP-{prefix}-{number:03d}'
        number += 1
        compact = sorted(set(re.findall(r'[A-Za-z]{16,}',
            ' '.join((title,task,fixture,expected,boundary)))))
        status = 'draft' if compact else 'published'
        parent = previous if previous and previous['level'] in (level,level-1) else (
            latest.get(max(level-1,0)) or latest.get(level))
        if not parent:
            raise ValueError('No published bridge for '+ident)
        problem = {
            'id':ident, 'tool_id':tool, 'title':title, 'level':level,
            'difficulty':f'level_{level}', 'scenario':task, 'task':task,
            'learning_objective':title,
            'inputs':{'fixture_contract':fixture,'environment':
                'Synthetic fixtures in an isolated learner-owned training target; record runtime versions and actual observations.'},
            'expected_output':{'contract':expected},
            'constraints':[boundary,
                'Preserve source attempts and unrelated files; never expose credentials or modify shared targets.'],
            'acceptance_criteria':['Demonstrate the specified result: '+expected,
                'Verify the stated boundary or failure: '+boundary,
                'Submit actual code or configuration, observed results and all help used.'],
            'prerequisites':[parent['id']], 'independent_prerequisites':[],
            'skill_prerequisites':[] if level == 0 else [f'{tool} bounded level {level-1}'],
            'progressive_hints':['Write the expected output for the smallest supplied input before changing code.',
                'Test this boundary on a separate copy: '+boundary,
                'Compare the actual result with '+expected+' and preserve failed evidence.'],
            'engineering_relevance':title+' is a bounded ingestion, warehouse or support responsibility. After review, explain the affected consumer and one untested operating limit.',
            'estimated_minutes':10 if level == 0 else min(180,15+level*12),
            'official_docs':DOCS[tool], 'verification':{'kind':'artifact_review'},
            'challenge_kind':'initial' if level == 0 else 'skill_build',
            'publication_status':status,
            'draft_reason':'Authoring stopped before a readability review; compressed prose requires precise rewriting.' if compact else None,
            'published_version':'2026.10.26.4', 'sequence':level*1000+number,
            'authoring_batch':'foundations-interrupted-explicit-003',
        }
        result.append(problem)
        if status == 'published':
            previous = problem
            latest[level] = problem
    return result

def main():
    summary = {}
    for tool, rows in ROWS.items():
        authored = build(tool, rows)
        path = BANK/f'{tool}-batch3.json'
        if path.exists():
            prior = json.loads(path.read_text(encoding='utf-8'))
            current = {p['id']:p for p in authored}
            for old in prior:
                if old['id'] not in current or current[old['id']]['title'].casefold().replace(' ','') != old['title'].casefold().replace(' ',''):
                    raise ValueError('Refusing ID deletion or reassignment: '+old['id'])
        body = json.dumps(authored,indent=2,ensure_ascii=False)+'\n'
        path.write_text(body,encoding='utf-8')
        counts = Counter(p['publication_status'] for p in authored)
        summary[tool] = {
            'prepared':len(authored),'publishable':counts['published'],'draft':counts['draft'],
            'sha256':hashlib.sha256(body.encode()).hexdigest(),
            'last_id':authored[-1]['id'],
            'next_id':f"{authored[-1]['id'].rsplit('-',1)[0]}-{int(authored[-1]['id'].rsplit('-',1)[1])+1:03d}"}
    checkpoint = {'status':'interrupted_agent_content_recovered_with_drafts',
        'source':'foundations_batch3.py','summary':summary,
        'quality_rule':'Compressed prose remains draft even when schema valid.',
        'next_action':'Rewrite drafts with precise readable contracts before promotion; preserve all IDs.'}
    (BANK/'authors/foundations-batch3-checkpoint.json').write_text(
        json.dumps(checkpoint,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
