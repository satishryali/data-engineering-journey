"""Completion regressions use disposable records, never synthetic live assessments."""
from datetime import date, datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urljoin,urlsplit
import test_recalllab as fixtures
from services.routing import app_url,resolve
from services.notes import headings,section,render_links,blocks
from services.records import Records,IST,load_coach,metrics
from services.journal import Journal
from services.sessions import get_plan,varied_question
from services.evaluation import manual_assessment,sql_assessment
from services.bridge import end_session
from services.ai import explain


class RoutingNotesTests(unittest.TestCase):
    def test_extra_study_has_the_deepest_green(self):
        from components.calendar import COLORS
        def luminance(color):
            return sum(weight*int(color[start:start+2],16) for weight,start in ((.2126,1),(.7152,3),(.0722,5)))
        self.assertLess(luminance(COLORS[-1]),min(luminance(c) for c in COLORS[1:-1]))

    def test_missed_days_break_current_streak_without_erasing_longest(self):
        activity = {}
        for day in range(1,6):
            activity[date(2026,10,day)] = {'seconds':3600 if day in (1,2) else 0,'events':[],'coding':[],'revisions':[],'intervals':[]}
        result = metrics(activity)
        self.assertEqual(result['longest_streak'],2)
        self.assertEqual(result['current_streak'],0)
        self.assertEqual(result['active_days'],2)

    def test_note_image_markup_inside_code_is_not_loaded(self):
        content = '```python\n![untrusted](../../outside.png)\n```\n'
        result = list(blocks(Records(),'Notes/README.md',content))
        self.assertEqual(result,[('markdown',content)])
        result = list(blocks(Records(),'Notes/README.md','![](https://external.invalid/tracker.png)\n'))
        self.assertEqual(result[0][0],'caption')
    def test_root_links_cannot_inherit_a_markdown_path(self):
        url = app_url('Coding Challenges',challenge='sql-count')
        self.assertEqual(urlsplit(urljoin('http://127.0.0.1:8501/list-plus.md',url)).path,'/')
        self.assertEqual(resolve({'view':'Coding Challenges','note':'old.md'}),'Coding Challenges')
        self.assertEqual(resolve({'view':'../../../bad'}),'Dashboard')

    def test_note_sections_ignore_code_headings_and_internal_links_use_router(self):
        text = '# Root\nPurpose\n## One\n```python\n# not a heading\nprint(1)\n```\n## Two\nOther\n'
        self.assertEqual(len(headings(text)),3)
        self.assertIn('print(1)',section(text,'Root / One'))
        self.assertNotIn('Other',section(text,'Root / One'))
        out = render_links(Records(),'Notes/New Syntax/README.md','[Lists](list-plus.md)\n[[revision/questions|Recall]]\n```\n[Lists](list-plus.md)\n```\n')
        self.assertIn('/?view=Notes+Browser',out)
        self.assertIn('note=Notes%2FNew+Syntax%2Flist-plus.md',out)
        self.assertIn('```\n[Lists](list-plus.md)',out)

    def test_overlapping_closed_intervals_are_merged_across_ist_midnight(self):
        rows = [dict(status='completed',start_time_ist='2026-10-17T23:30:00+05:30',end_time_ist='2026-10-18T00:30:00+05:30'),
                dict(status='completed',start_time_ist='2026-10-18T00:00:00+05:30',end_time_ist='2026-10-18T01:00:00+05:30'),
                dict(status='uncertain',start_time_ist='2026-10-18T01:00:00+05:30',end_time_ist='2026-10-18T04:00:00+05:30')]
        r = Records()
        with patch.object(r,'csv',return_value=rows),patch.object(r,'events',return_value=[]):
            activity = r.activity(date(2026,10,18))
        self.assertEqual(activity[date(2026,10,17)]['seconds'],1800)
        self.assertEqual(activity[date(2026,10,18)]['seconds'],3600)

    def test_local_ai_requires_opt_in_and_rejects_remote_endpoints(self):
        with patch('services.ai.build_opener') as network:
            self.assertIn('off',explain('http://127.0.0.1:11434','model','note','q','a'))
            network.assert_not_called()
            with self.assertRaises(ValueError):
                explain('https://external.example','model','note','q','a',True)
            network.assert_not_called()


class CompletionPersistenceTests(unittest.TestCase):
    setUp = fixtures.BridgeTests.setUp
    payload = fixtures.BridgeTests.payload

    def test_plan_freezes_survives_restart_changes_formats_and_extends(self):
        first = get_plan(self.records,self.journal,self.session,20,date(2026,10,18))
        self.assertGreaterEqual(len(first['tasks']),2)
        self.assertEqual(first,get_plan(self.records,Journal(self.journal.path),self.session,20,date(2026,10,19)))
        later = get_plan(self.records,self.journal,'another-session',20,date(2026,10,19))
        self.assertNotEqual(first['tasks'][0]['question']['mode'],later['tasks'][0]['question']['mode'])
        extended = get_plan(self.records,self.journal,self.session,30,date(2026,10,18))
        self.assertEqual(extended['tasks'][:len(first['tasks'])],first['tasks'])
        self.assertGreater(len(extended['tasks']),len(first['tasks']))
        self.assertTrue(any(t['runner'] for t in first['tasks']))
        self.assertTrue(all(t['question']['sources'] for t in first['tasks']))

    def test_human_assessment_preserves_original_unknown_help_and_replays(self):
        a = self.journal.save(self.session,'manual',dict(self.payload(),score=None,result='unknown',help_used=None,evaluation='manual_pending'))
        review = dict(reviewer='Test reviewer',verification='Synthetic observed checks in a disposable test.',feedback='Fixture review only.',score=3)
        self.journal.assess(a['attempt_id'],review)
        self.journal.assess(a['attempt_id'],review)
        effective = self.journal.effective_attempts()[0]
        self.assertIsNone(effective['score'])
        self.assertEqual(effective['result'],'unknown')
        self.assertIsNone(effective['original_submission']['score'])
        self.assertEqual(self.journal.attempts()[0]['answer'],a['answer'])
        with self.assertRaises(ValueError):
            self.journal.assess(a['attempt_id'],dict(review,feedback='Conflicting review'))
        end_session(self.records,self.journal,self.session)
        event = self.records.events()[-1]
        self.assertNotEqual(event['review_kind'],'delayed')
        self.assertEqual(event['evaluation'],'human_review')
        self.assertIn('Validated',load_coach(self.root).validate(self.root))

    def test_manual_verified_success_uses_assessment_date_without_delayed_claim(self):
        old = datetime(2026,10,17,12,tzinfo=IST)
        with patch('services.journal.now',return_value=old):
            a = self.journal.save(self.session,'old-code',dict(self.payload('py.records.cleaning'),score=None,evaluation='manual_pending'))
        self.journal.assess(a['attempt_id'],dict(reviewer='Fixture reviewer',verification='Observed all expected outputs.',feedback='Sound output checks.',score=3))
        end_session(self.records,self.journal,self.session)
        event = self.records.events()[-1]
        self.assertEqual(event['review_kind'],'application')
        self.assertEqual(event['submitted_date_ist'],'2026-10-17')
        self.assertEqual(event['original_submission']['timestamp'],old.isoformat())
        self.assertEqual(event['score'],3)

    def test_import_idempotence_and_conflict_preservation(self):
        self.journal.save(self.session,'token',self.payload())
        self.journal.put('drafts','draft',{'answer':'original'})
        export = self.journal.export()
        target = Journal(self.root/'imported.sqlite3')
        target.restore_export(export); target.restore_export(export)
        self.assertEqual(len(target.attempts()),1)
        self.assertEqual(target.session(),self.session)
        conflict = Journal(self.root/'conflict.sqlite3')
        conflict.put('drafts','draft',{'answer':'local changes'})
        with self.assertRaises(ValueError):
            conflict.restore_export(export)
        self.assertEqual(conflict.attempts(),[])
        self.assertEqual(conflict.get('drafts','draft')['answer'],'local changes')

    def test_imported_frozen_checkpoint_recreates_missing_evidence(self):
        self.journal.save(self.session,'token',self.payload())
        coach = load_coach(self.root)
        with patch('services.bridge.load_coach',return_value=coach),patch.object(coach,'record',side_effect=OSError('Interrupted before record')):
            with self.assertRaises(OSError):
                end_session(self.records,self.journal,self.session)
        for p in (self.root/'apps/recalllab/evidence').glob('*.json'):
            p.unlink()  # disposable fixture only
        imported = Journal(self.root/'restored.sqlite3')
        imported.restore_export(self.journal.export())
        end_session(self.records,imported,self.session)
        self.assertEqual(len(list((self.root/'apps/recalllab/evidence').glob('*.json'))),1)
        self.assertIn('Validated',coach.validate(self.root))

    def test_sql_partial_evaluation_and_assistance_are_honest(self):
        partial = sql_assessment({'passed':False,'fixtures':[{'passed':True},{'passed':False}],'error':None},False)
        self.assertEqual(partial['evaluation_status'],'partially_correct')
        self.assertEqual(partial['score'],1)
        self.assertEqual(partial['result'],'needs_guidance')
        passed = {'passed':True,'fixtures':[{'passed':True}]*3,'error':None}
        self.assertIsNone(sql_assessment(passed,None)['score'])
        self.assertEqual(sql_assessment(passed,False,True)['result'],'assisted')


if __name__=='__main__':
    unittest.main()
