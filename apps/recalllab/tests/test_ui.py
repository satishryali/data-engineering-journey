"""UI tests use a disposable checkout. Synthetic submissions never touch live history."""
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from services.records import ROOT
from streamlit.testing.v1 import AppTest


class UITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('tracking', 'Notes', 'tools', 'progress', 'plan', 'projects'):
            shutil.copytree(ROOT / folder, self.root / folder, ignore=shutil.ignore_patterns('__pycache__', 'node_modules', '.obsidian', 'tests', '*.coach-tmp', '.coach-transaction.json'))
        for file in ('START-HERE.md', 'AGENTS.md'):
            shutil.copy2(ROOT / file, self.root / file)
        self.env = patch.dict(os.environ, {'RECALLLAB_ROOT': str(self.root), 'RECALLLAB_DATA': str(self.root / 'apps/recalllab/data')})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_all_pages_render_and_dashboard_navigation(self):
        app = AppTest.from_file(str(APP / 'app.py'), default_timeout=20).run()
        self.assertFalse(app.exception)
        app.query_params['view'] = "Today's Session"
        app.run()
        self.assertFalse(app.exception)
        for page in ['Dashboard', "Today's Session", 'Question Bank', 'Coding Challenges', 'Notes Browser',
                     'Mistakes & Weak Topics', 'Progress & Analytics', 'Revision Calendar', 'Search Notes', 'Settings',
                     'Learning Roadmap', 'Project', 'Interview Practice']:
            app.radio(key='route').set_value(page).run()
            self.assertFalse(app.exception, (page, list(app.exception)))

    def test_azure_schedule_and_interview_pages_preserve_records(self):
        from datetime import datetime
        from services.records import IST
        protected = ['tracking/study-log.csv', 'tracking/revision-queue.csv', 'tracking/revision-history.csv',
                     'tracking/mistakes.json', 'tracking/skill-state.json', 'progress/current.md', 'START-HERE.md']
        before = {p: (self.root/p).read_bytes() for p in protected}
        with patch('services.records.now', return_value=datetime(2026,10,22,12,tzinfo=IST)):
            app = AppTest.from_file(str(APP/'app.py'), default_timeout=20).run()
            self.assertFalse(app.exception)
            self.assertEqual(next(m.value for m in app.metric if m.label=='Daily target'), '7.00 h')
            self.assertEqual(next(m.value for m in app.metric if m.label=='Week target'), '52.00 h')
            app.radio(key='route').set_value('Learning Roadmap').run()
            self.assertEqual(len(app.dataframe[0].value), 13)
            self.assertTrue(all(app.dataframe[0].value['status']=='planned'))
            app.radio(key='route').set_value('Interview Practice').run()
            self.assertFalse(app.exception)
            self.assertFalse(app.text_area)
            self.assertFalse(any('solution' in exp.label.lower() for exp in app.expander))
            app.selectbox[0].set_value('INT-DELTA-001').run()
            self.assertFalse(app.exception)
        self.assertEqual({p: (self.root/p).read_bytes() for p in protected}, before)

    def test_submit_hint_retry_and_checkpoint_in_browser(self):
        app = AppTest.from_file(str(APP / 'app.py'), default_timeout=20).run()
        app.radio(key='route').set_value("Today's Session").run()
        app.radio(key='practice-mode').set_value('Extra concept practice').run()
        # Select output prediction with an automatically verifiable answer.
        app.selectbox[0].set_value('py.dict.access').run()
        app.text_area[0].set_value('[]').run()
        next(b for b in app.button if b.label == 'Submit Attempt').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Saved locally' in s.value for s in app.success))
        self.assertTrue(any('End session' in b.label for b in app.button))
        next(b for b in app.button if b.label == 'End session / save checkpoint').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertTrue((self.root / 'apps/recalllab/evidence').exists())

    def test_dashboard_links_route_to_specific_note_and_task(self):
        app = AppTest.from_file(str(APP / 'app.py'), default_timeout=20)
        app.query_params['view'] = "Today's Session"
        app.query_params['item'] = 'py.csv.read'
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value, 'py.csv.read')
        app.query_params.clear()
        app.query_params['view'] = 'Notes Browser'
        app.query_params['note'] = 'Notes/Python/Concepts/csv-reading.md'
        app.query_params['heading'] = 'Read a CSV file'
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value, 'Notes/Python/Concepts/csv-reading.md')

    def test_revision_calendar_defaults_to_revision_not_study(self):
        # Empty review evidence in this disposable checkout, regardless of future live study.
        from services.records import load_coach
        coach = load_coach(self.root)
        fields, _ = coach.read_csv(self.root, 'tracking/revision-history.csv')
        (self.root/'tracking/revision-history.csv').write_text(coach.csv_text(fields, []), encoding='utf-8')
        app = AppTest.from_file(str(APP / 'app.py'), default_timeout=20)
        app.query_params['view'] = 'Revision Calendar'
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value, 'Revision Only')
        self.assertTrue(any('Revision has not started yet' in i.value for i in app.info))
        attempts = next(m for m in app.metric if m.label == 'Revision attempts')
        self.assertEqual(attempts.value, '0')

    def test_sidebar_clears_stale_note_url_and_survives_refresh(self):
        app = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        app.query_params.update({'view':'Notes Browser','note':'Notes/New Syntax/list-plus.md'})
        app.run()
        app.radio(key='route').set_value('Coding Challenges').run()
        self.assertFalse(app.exception)
        self.assertEqual(app.query_params['view'],'Coding Challenges')
        self.assertNotIn('note',app.query_params)
        self.assertTrue(any(t.value=='Coding Challenges' for t in app.title))
        restarted = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        restarted.query_params.update(dict(app.query_params))
        restarted.run()
        self.assertFalse(restarted.exception)
        self.assertEqual(restarted.radio(key='route').value,'Coding Challenges')
        self.assertTrue(any(s.label=='Challenge' for s in restarted.selectbox))
        self.assertFalse(any(s.label=='Original note' for s in restarted.selectbox))

    def test_daily_draft_and_next_task_survive_restart(self):
        app = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        app.query_params['view']="Today's Session"
        app.run()
        app.text_area[0].set_value('Disposable fixture draft').run()
        self.assertFalse(app.exception)
        restarted = AppTest.from_file(str(APP/'app.py'),default_timeout=20).run()
        self.assertFalse(restarted.exception)
        self.assertEqual(restarted.text_area[0].value,'Disposable fixture draft')
        next(b for b in restarted.button if b.label=='Submit Attempt').click().run()
        self.assertFalse(restarted.exception)
        next(b for b in restarted.button if b.label=='Next Task').click().run()
        self.assertFalse(restarted.exception)
        self.assertEqual(next(s for s in restarted.selectbox if s.label=="Today's task").value,1)
        final = AppTest.from_file(str(APP/'app.py'),default_timeout=20).run()
        self.assertEqual(next(s for s in final.selectbox if s.label=="Today's task").value,1)

    def test_calendar_filter_and_day_survive_reload(self):
        from datetime import date
        app = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        app.query_params['view']='Revision Calendar'
        app.run()
        next(s for s in app.selectbox if s.label=='Activity metric').set_value('Coding Practice').run()
        app.date_input[0].set_value(date(2026,10,16)).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.query_params['metric'],'Coding Practice')
        self.assertEqual(app.query_params['day'],'2026-10-16')
        reload = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        reload.query_params.update(dict(app.query_params)); reload.run()
        self.assertFalse(reload.exception)
        self.assertEqual(reload.selectbox[0].value,'Coding Practice')
        self.assertEqual(reload.date_input[0].value,date(2026,10,16))

    def test_human_review_form_and_completed_report(self):
        app = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        app.query_params.update({'view':"Today's Session",'item':'py.records.cleaning'})
        app.run()
        app.text_area[0].set_value('Synthetic manual-review fixture; never learner evidence.').run()
        next(r for r in app.radio if r.label=='Other help used?').set_value('No help').run()
        next(b for b in app.button if b.label=='Submit Attempt').click().run()
        next(t for t in app.text_input if t.label=='Reviewer name / role').set_value('Fixture reviewer')
        next(t for t in app.text_area if t.label=='Observed output, edge-case checks or reasoning evidence').set_value('Synthetic expected-output verification for the test only.')
        next(t for t in app.text_area if t.label=='Specific feedback and next action').set_value('Fixture human review; no code execution occurred.')
        next(s for s in app.selectbox if s.label=='Rubric score').set_value(3)
        app.checkbox[0].check()
        next(b for b in app.button if b.label=='Save human assessment').click().run()
        self.assertFalse(app.exception)
        next(b for b in app.button if b.label=='End session / save checkpoint').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertTrue(any('Notes to Review' in e.label for e in app.expander))

    def test_coding_language_and_challenge_filters_survive_refresh(self):
        from challenges.catalog import SQL
        app = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        app.query_params['view']='Coding Challenges'
        app.run()
        app.radio(key='coding-language-filter').set_value('SQL (disposable SQLite)').run()
        app.selectbox(key='coding-challenge-filter').set_value(SQL[2]).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.query_params['language'],'SQL')
        self.assertEqual(app.query_params['challenge'],'sql-sum')
        reload = AppTest.from_file(str(APP/'app.py'),default_timeout=20)
        reload.query_params.update(dict(app.query_params)); reload.run()
        self.assertFalse(reload.exception)
        self.assertEqual(reload.radio(key='coding-language-filter').value,'SQL (disposable SQLite)')
        self.assertEqual(reload.selectbox(key='coding-challenge-filter').value[0],'sql-sum')


if __name__ == '__main__':
    unittest.main()
