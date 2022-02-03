import time
from unittest import TestCase, mock

from gobapi.profiled_query import ProfiledQuery, activate


class MockEvent:
    calls = 0

    def listens_for(self, *args, **kwargs):
        MockEvent.calls += 1

        def before_after_cursor_execute(func):
            func(mock.MagicMock(), None, "any statement", None, None, None)

        return before_after_cursor_execute


class TestProfiledQuery(TestCase):

    def test_profiled_query(self):
        q = ProfiledQuery("any statement")
        q.set_start()
        q.set_end()

        duration = q.duration
        self.assertTrue(duration >= 0)

        q.start_time = 0
        q.end_time = q.start_time + ProfiledQuery.LONG_DURATION
        self.assertFalse(q.is_slow)
        q.end_time = q.start_time + ProfiledQuery.LONG_DURATION + 1
        self.assertTrue(q.is_slow)

        # assert log message for slow query is correct
        # use localtime for different tz settings
        expected = f"""ProfiledQuery
Statement: any statement
Duration:  30 minutes
Started:   {time.strftime("%H:%M:%S", time.localtime(q.start_time))}
Ended:     {time.strftime("%H:%M:%S", time.localtime(q.end_time))}
"""
        self.assertEqual(str(q), expected)

    @mock.patch("gobapi.profiled_query.event", MockEvent())
    def test_activate(self):
        activate()
        self.assertEqual(MockEvent.calls, 2)
