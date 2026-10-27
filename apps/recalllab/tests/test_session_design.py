"""Recall interaction regressions run against disposable learner records."""
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import test_ui as ui_fixtures
import test_recalllab as record_fixtures
from streamlit.testing.v1 import AppTest
from services.journal import Journal
from services.sessions import get_plan


class RecallInteractionTests(unittest.TestCase):
    setUp = ui_fixtures.UITests.setUp

    def open_session(self):
        app = AppTest.from_file(str(ui_fixtures.APP/'app.py'),default_timeout=20)
        app.query_params['view'] = "Today's Session"
        return app.run()

    def test_reveal_requires_saved_attempt_and_confirmation(self):
        app = self.open_session()
        self.assertFalse(app.exception)
        submit = next(b for b in app.button if b.label=='Submit Attempt')
        self.assertTrue(submit.disabled)
        self.assertFalse(any(b.label=='Reveal answer' for b in app.button))
        app.text_area[0].set_value('My incomplete retrieval attempt').run()
        next(b for b in app.button if b.label=='Submit Attempt').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(next(b for b in app.button if b.label=='Reveal answer').disabled)
        next(c for c in app.checkbox if 'recall attempt' in c.label).check().run()
        next(b for b in app.button if b.label=='Reveal answer').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(m.value=='#### Worked reference' for m in app.markdown))

    def test_pause_and_resume_keep_draft_after_restart(self):
        app = self.open_session()
        app.text_area[0].set_value('Draft saved across a break').run()
        next(b for b in app.button if b.label=='Pause session').click().run()
        self.assertFalse(app.exception)
        restarted = self.open_session()
        self.assertFalse(restarted.text_area)
        self.assertTrue(any('paused' in i.value for i in restarted.info))
        next(b for b in restarted.button if b.label=='Resume revision').click().run()
        self.assertFalse(restarted.exception)
        self.assertEqual(restarted.text_area[0].value,'Draft saved across a break')

    def test_difficulty_is_durable_without_mutating_assessment(self):
        app = self.open_session()
        app.text_area[0].set_value('Recall self-report fixture').run()
        next(b for b in app.button if b.label=='Submit Attempt').click().run()
        journal = Journal(self.root/'apps/recalllab/data/recalllab.sqlite3')
        before = journal.attempts()
        next(r for r in app.radio if r.label=='How did recall feel?').set_value('Recalled with difficulty').run()
        self.assertFalse(app.exception)
        restarted = self.open_session()
        self.assertEqual(next(r for r in restarted.radio if r.label=='How did recall feel?').value,'Recalled with difficulty')
        self.assertEqual(journal.attempts(),before)


class DailyLimitTests(unittest.TestCase):
    setUp = record_fixtures.BridgeTests.setUp

    def test_limit_bounds_new_work_and_never_truncates_saved_tasks(self):
        first = get_plan(self.records,self.journal,self.session,60,date(2026,10,18),max_items=2)
        self.assertEqual(len(first['tasks']),2)
        restored = get_plan(self.records,Journal(self.journal.path),self.session,60,date(2026,10,19),max_items=1)
        self.assertEqual(first,restored)
        bigger = get_plan(self.records,self.journal,'larger',60,date(2026,10,18),max_items=5)
        self.assertEqual(len(bigger['tasks']),5)
        self.assertEqual(get_plan(self.records,self.journal,'larger',60,max_items=1)['tasks'],bigger['tasks'])


if __name__=='__main__':
    unittest.main()
