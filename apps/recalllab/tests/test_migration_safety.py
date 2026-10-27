"""Migration snapshots are restorable; future journals are never downgraded."""
import hashlib
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.journal import Journal


class MigrationSafetyTests(unittest.TestCase):
    def test_backup_contains_original_schema_and_rows_before_migration(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'journal.sqlite3'
            with closing(sqlite3.connect(path)) as db:
                db.execute('CREATE TABLE sessions(id TEXT PRIMARY KEY, created TEXT NOT NULL)')
                db.execute("INSERT INTO sessions VALUES('legacy','2026-10-25')")
                db.commit()
            journal = Journal(path)
            backups = list(path.parent.glob('backup-pre-v2-*.sqlite3'))
            self.assertEqual(len(backups), 1)
            with closing(sqlite3.connect(backups[0])) as db:
                self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 0)
                self.assertEqual(len(db.execute('PRAGMA table_info(sessions)').fetchall()), 2)
                self.assertEqual(db.execute('SELECT id FROM sessions').fetchone()[0], 'legacy')
            self.assertEqual(journal.sessions()[0]['state'], 'open')
            Journal(path)
            self.assertEqual(len(list(path.parent.glob('backup-pre-v2-*.sqlite3'))), 1)

    def test_future_schema_refused_without_modifying_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'journal.sqlite3'
            with closing(sqlite3.connect(path)) as db:
                db.execute('PRAGMA user_version=99')
            before = hashlib.sha256(path.read_bytes()).digest()
            with self.assertRaisesRegex(ValueError, 'newer schema'):
                Journal(path)
            self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), before)


if __name__ == '__main__':
    unittest.main()
