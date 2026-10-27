"""Redesign regression checks. All writes use disposable local data/checkouts."""
from datetime import date
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from services.journal import Journal
from services.records import ROOT, Records
from services.sessions import get_plan
from streamlit.testing.v1 import AppTest


class BoundedPlanTests(unittest.TestCase):
    def test_limit_survives_restart_and_larger_requested_budget(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.sqlite3'
            journal = Journal(path)
            session = journal.session()
            first = get_plan(Records(), journal, session, 60, date(2026, 10, 26), max_items=2)
            self.assertEqual(len(first['tasks']), 2)
            restarted = Journal(path)
            resumed = get_plan(Records(), restarted, session, 60, date(2026, 10, 27), max_items=2)
            self.assertEqual(resumed, first)
            self.assertEqual(restarted.attempts(), [])

    def test_lowering_limit_preserves_saved_tasks_and_drafts(self):
        with tempfile.TemporaryDirectory() as folder:
            journal = Journal(Path(folder) / 'test.sqlite3')
            session = journal.session()
            first = get_plan(Records(), journal, session, 60, date(2026, 10, 26), max_items=5)
            self.assertEqual(len(first['tasks']), 5)
            journal.put('drafts', 'fixture', {'answer': 'keep my unfinished answer'})
            resumed = get_plan(Records(), journal, session, 60, date(2026, 10, 27), max_items=1)
            self.assertEqual(resumed, first)
            self.assertEqual(journal.get('drafts', 'fixture')['answer'], 'keep my unfinished answer')


class FocusedSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('tracking', 'Notes', 'tools', 'progress', 'plan', 'projects'):
            shutil.copytree(ROOT / folder, self.root / folder,
                            ignore=shutil.ignore_patterns('__pycache__', 'node_modules', '.obsidian', 'tests', '*.coach-tmp', '.coach-transaction.json'))
        for file in ('START-HERE.md', 'AGENTS.md'):
            shutil.copy2(ROOT / file, self.root / file)
        self.data = self.root / 'apps/recalllab/data'
        env = patch.dict(os.environ, {'RECALLLAB_ROOT': str(self.root), 'RECALLLAB_DATA': str(self.data)})
        env.start()
        self.addCleanup(env.stop)

    def app(self):
        app = AppTest.from_file(str(APP / 'app.py'), default_timeout=25)
        app.query_params['view'] = "Today's Session"
        app.run()
        self.assertFalse(app.exception)
        return app

    def test_pause_and_resume_survive_process_restart_without_scoring(self):
        app = self.app()
        app.text_area[0].set_value('Unfinished synthetic answer').run()
        next(b for b in app.button if b.label == 'Pause session').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.text_area)
        restarted = self.app()
        self.assertTrue(any(b.label == 'Resume revision' for b in restarted.button))
        next(b for b in restarted.button if b.label == 'Resume revision').click().run()
        self.assertFalse(restarted.exception)
        self.assertEqual(restarted.text_area[0].value, 'Unfinished synthetic answer')
        self.assertEqual(Journal(self.data / 'recalllab.sqlite3').attempts(), [])

    def test_empty_submission_does_not_unlock_reference_or_save_attempt(self):
        app = self.app()
        self.assertFalse(any('reference' in b.label.lower() or 'reveal' in b.label.lower() for b in app.button))
        self.assertTrue(next(b for b in app.button if b.label == 'Submit Attempt').disabled)
        self.assertEqual(Journal(self.data / 'recalllab.sqlite3').attempts(), [])
        self.assertFalse(any('reference' in b.label.lower() or 'reveal' in b.label.lower() for b in app.button))

    def test_submit_then_reveal_preserves_original_attempt_and_project_records(self):
        protected = ('tracking/study-log.csv', 'tracking/revision-history.csv', 'tracking/revision-queue.csv',
                     'tracking/mistakes.json', 'tracking/skill-state.json', 'progress/current.md', 'START-HERE.md',
                     'projects/rrdap/checkpoint.md', 'projects/rrdap/tasks/RDS-001.md')
        before = {p: (self.root / p).read_bytes() for p in protected}
        app = self.app()
        app.text_area[0].set_value('Synthetic QA recall attempt; no learner evidence.').run()
        next(b for b in app.button if b.label == 'Submit Attempt').click().run()
        self.assertFalse(app.exception)
        journal = Journal(self.data / 'recalllab.sqlite3')
        original = journal.attempts()
        self.assertEqual(len(original), 1)
        self.assertTrue(next(b for b in app.button if b.label == 'Reveal answer').disabled)
        next(c for c in app.checkbox if c.label == 'I made a recall attempt before checking the reference').check().run()
        reveal = next(b for b in app.button if b.label == 'Reveal answer')
        reveal.click().run()
        self.assertFalse(app.exception)
        self.assertEqual(journal.attempts(), original)
        next(r for r in app.radio if r.label == 'How did recall feel?').set_value('Recalled with difficulty').run()
        restarted = self.app()
        self.assertEqual(next(r for r in restarted.radio if r.label == 'How did recall feel?').value, 'Recalled with difficulty')
        self.assertEqual(journal.attempts(), original)
        self.assertEqual({p: (self.root / p).read_bytes() for p in protected}, before)


if __name__ == '__main__':
    unittest.main()
