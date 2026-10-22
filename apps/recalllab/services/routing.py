"""One allowlisted root URL format for widgets, cards, calendar and note links."""
import json
from urllib.parse import urlencode

PAGES = ['Dashboard', "Today's Session", 'Question Bank', 'Coding Challenges', 'Notes Browser',
         'Mistakes & Weak Topics', 'Progress & Analytics', 'Revision Calendar', 'Search Notes', 'Settings']


def app_url(page='Dashboard', **values):
    if page not in PAGES:
        raise ValueError('Unknown page')
    return '/?' + urlencode({'view':page, **{k:str(v) for k,v in values.items() if v is not None}})


def fingerprint(query):
    return json.dumps(dict(query), sort_keys=True)


def resolve(query, fallback='Dashboard'):
    value = query.get('view', fallback)
    return value if value in PAGES else 'Dashboard'
