"""Durable local drafts/submissions. No canonical write until explicit end-session."""
from contextlib import contextmanager, closing
import json
from pathlib import Path
import sqlite3
import uuid
import re
from services.records import ROOT, now


class Journal:
    SCHEMA_VERSION = 2

    def __init__(self, path=None):
        self.path = Path(path or ROOT / 'apps/recalllab/data/recalllab.sqlite3')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Inspect and snapshot existing data before any DDL, including CREATE TABLE.
        # SQLite's backup API includes committed WAL data and leaves the source intact.
        if self.path.exists() and self.path.stat().st_size:
            with closing(sqlite3.connect(self.path, timeout=20)) as source:
                version = source.execute('PRAGMA user_version').fetchone()[0]
                if version > self.SCHEMA_VERSION:
                    raise ValueError('This journal uses a newer schema. Update RecallLab before opening it.')
                if version < self.SCHEMA_VERSION:
                    backup = self.path.with_name(f'backup-pre-v{self.SCHEMA_VERSION}-{uuid.uuid4().hex}.sqlite3')
                    with closing(sqlite3.connect(backup)) as destination:
                        source.backup(destination)
        with self.db() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, created TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'open', batch TEXT);
                CREATE TABLE IF NOT EXISTS attempts(id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id), token TEXT UNIQUE NOT NULL, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS drafts(key TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS assessments(attempt_id TEXT PRIMARY KEY REFERENCES attempts(id), payload TEXT NOT NULL);
            ''')
            self._migrate(db)

    def _migrate(self, db):
        """Bring older local journals forward without rewriting user payloads."""
        columns = {row['name'] for row in db.execute('PRAGMA table_info(sessions)')}
        if 'state' not in columns:
            db.execute("ALTER TABLE sessions ADD COLUMN state TEXT NOT NULL DEFAULT 'open'")
        if 'batch' not in columns:
            db.execute('ALTER TABLE sessions ADD COLUMN batch TEXT')
        db.execute('CREATE INDEX IF NOT EXISTS idx_attempts_session ON attempts(session_id)')
        db.execute('CREATE INDEX IF NOT EXISTS idx_assessments_attempt ON assessments(attempt_id)')
        db.execute(f'PRAGMA user_version={self.SCHEMA_VERSION}')

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.path, timeout=20)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA synchronous=FULL')
        try:
            with db:
                yield db
        finally:
            db.close()

    def session(self):
        with self.db() as db:
            # Serialize the read-then-create sequence when two browser tabs open together.
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT * FROM sessions WHERE state='open' ORDER BY created DESC LIMIT 1").fetchone()
            if row:
                return row['id']
            ident = 'RL-' + uuid.uuid4().hex
            db.execute('INSERT INTO sessions(id,created) VALUES(?,?)', (ident, now().isoformat()))
            return ident

    def save(self, session, token, payload):
        if not payload.get('answer', '').strip() or not payload.get('question', '').strip():
            raise ValueError('An actual question and nonempty answer are required')
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT payload FROM attempts WHERE token=?', (token,)).fetchone()
            if old:
                previous = json.loads(old[0])
                if any(previous.get(k) != v for k, v in payload.items()):
                    raise ValueError('Submission already saved; use a changed-example retry for a new attempt')
                return previous
            row = db.execute('SELECT state FROM sessions WHERE id=?', (session,)).fetchone()
            if row is None or row[0] != 'open':
                raise ValueError('Session is frozen; finish checkpoint recovery before adding attempts')
            ident = 'ATT-RL-' + uuid.uuid4().hex
            stamp = now()
            saved = dict(payload, attempt_id=ident, review_id='REV-' + ident, timestamp=stamp.isoformat())
            saved['attempt_date_ist'] = stamp.date().isoformat()
            saved['app_session_id'] = session
            db.execute('INSERT INTO attempts VALUES(?,?,?,?)', (ident, session, token, json.dumps(saved)))
            return saved

    def attempts(self, session=None):
        with self.db() as db:
            rows = db.execute('SELECT payload FROM attempts' + (' WHERE session_id=?' if session else '') + ' ORDER BY rowid', (session,) if session else ()).fetchall()
            return [json.loads(r[0]) for r in rows]

    def sessions(self):
        with self.db() as db:
            return [dict(r) for r in db.execute('SELECT * FROM sessions ORDER BY created DESC')]

    def assess(self, attempt_id, assessment):
        """Append one human assessment; original code/answer is never replaced."""
        from services.evaluation import manual_assessment
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT a.payload,s.state FROM attempts a JOIN sessions s ON s.id=a.session_id WHERE a.id=?', (attempt_id,)).fetchone()
            if not row or row['state'] != 'open':
                raise ValueError('Only open-session attempts can be assessed; checkpointed evidence is immutable.')
            original = json.loads(row['payload'])
            if original.get('evaluation') != 'manual_pending':
                raise ValueError('This attempt already has an executable evaluation.')
            result = manual_assessment(original, **assessment)
            previous = db.execute('SELECT payload FROM assessments WHERE attempt_id=?', (attempt_id,)).fetchone()
            if previous:
                prior = json.loads(previous[0])
                if any(prior.get(k) != v for k,v in result.items()):
                    raise ValueError('Assessment already saved. Preserve it and submit a new changed attempt.')
                return prior
            stamp = now()
            result.update(timestamp=stamp.isoformat(),attempt_date_ist=stamp.date().isoformat(),
                          submitted_date_ist=original['attempt_date_ist'])
            db.execute('INSERT INTO assessments VALUES(?,?)', (attempt_id,json.dumps(result)))
            return result

    def effective_attempts(self, session=None):
        attempts = self.attempts(session)
        with self.db() as db:
            annotations = {r[0]:json.loads(r[1]) for r in db.execute('SELECT * FROM assessments')}
        return [dict(a, **annotations[a['attempt_id']], original_submission=a) if a['attempt_id'] in annotations else a for a in attempts]

    def put(self, table, key, value):
        if table not in ('drafts', 'settings'):
            raise ValueError('Invalid local state table')
        with self.db() as db:
            db.execute(f'INSERT INTO {table} VALUES(?,?) ON CONFLICT(key) DO UPDATE SET payload=excluded.payload', (key, json.dumps(value)))

    def get(self, table, key, default=None):
        if table not in ('drafts', 'settings'):
            raise ValueError('Invalid local state table')
        with self.db() as db:
            row = db.execute(f'SELECT payload FROM {table} WHERE key=?', (key,)).fetchone()
            return json.loads(row[0]) if row else default

    def export(self):
        with self.db() as db:
            return json.dumps({'version': 1, 'exported': now().isoformat(),
                               **{t: [dict(r) for r in db.execute(f'SELECT * FROM {t}')] for t in ('sessions', 'attempts', 'drafts', 'settings', 'assessments')}}, indent=2)

    def restore_export(self, text):
        """Transactional import; exact replay is harmless, any conflict preserves both sources."""
        if len(text) > 20_000_000:
            raise ValueError('Export exceeds 20 MB; use a trusted SQLite backup instead.')
        data = json.loads(text)
        if data.get('version') != 1:
            raise ValueError('Unsupported recovery export version')
        tables = {'sessions':('id','created','state','batch'), 'attempts':('id','session_id','token','payload'),
                  'drafts':('key','payload'), 'settings':('key','payload'), 'assessments':('attempt_id','payload')}
        for row in data.get('sessions', []):
            if not re.fullmatch(r'RL-[a-f0-9]{32}', row.get('id','')) or row.get('state') not in ('open','pending','recorded'):
                raise ValueError('Invalid exported session')
            if row.get('batch'):
                batch = json.loads(row['batch'])
                allowed = {'checkpoint_id','date_ist','kind','summary','evidence_ids','reviews','skill_updates','mistakes'}
                if set(batch)-allowed or batch.get('checkpoint_id') != 'CP-'+row['id']:
                    raise ValueError('Unsupported frozen checkpoint fields')
                for event in batch.get('reviews', []):
                    if not re.fullmatch(r'ATT-RL-[a-f0-9]{32}', event.get('attempt_id','')) or event.get('evidence') != 'apps/recalllab/evidence/'+event['attempt_id']+'.json':
                        raise ValueError('Invalid frozen evidence path')
        for row in data.get('attempts', []):
            payload = json.loads(row['payload'])
            if not re.fullmatch(r'ATT-RL-[a-f0-9]{32}', row.get('id','')) or payload.get('attempt_id') != row['id'] or payload.get('review_id') != 'REV-'+row['id']:
                raise ValueError('Invalid exported attempt identity')
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            for table, columns in tables.items():
                for row in data.get(table, []):
                    if set(row) != set(columns):
                        raise ValueError('Invalid export table columns: '+table)
                    if 'payload' in row:
                        json.loads(row['payload'])
                    old = db.execute(f'SELECT * FROM {table} WHERE {columns[0]}=?',(row[columns[0]],)).fetchone()
                    if old and dict(old) != row:
                        raise ValueError('Import conflicts with local '+table+'; both originals are preserved. Restore into a separate local data directory.')
                    if not old:
                        db.execute(f'INSERT INTO {table}({",".join(columns)}) VALUES({",".join("?" for _ in columns)})', tuple(row[c] for c in columns))
        return 'Recovery journal imported locally. Pending attempts still require session completion; nothing was pushed.'

    def drafts(self):
        with self.db() as db:
            return [(r[0], json.loads(r[1])) for r in db.execute('SELECT key,payload FROM drafts')]

    def backup(self):
        target = self.path.parent / ('backup-' + now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6] + '.sqlite3')
        dest = sqlite3.connect(target)
        try:
            with self.db() as source:
                source.backup(dest)
        finally:
            dest.close()
        return target
