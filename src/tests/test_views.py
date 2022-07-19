from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from gobapi.views import initialise_api_views


class MockGOBViews:
    views = {
        'cata': {
            'ent1': {
                'view1': {
                    'name': 'view1name',
                    'query': 'view1query'
                },
                'view2': {
                    'name': 'view2name',
                    'query': 'view2query'
                }
            }
        },
        'catb': {
            'ent2': {
                'view3': {
                    'name': 'view3name',
                    'query': 'view3query'
                }
            }
        }
    }

    def get_catalogs(self):
        return self.views.keys()

    def get_entities(self, cat):
        return self.views[cat].keys()

    def get_views(self, cat, entity):
        return self.views[cat][entity]


class TestViews(TestCase):

    @patch("gobapi.views.GOBViews", MockGOBViews)
    def test_init_views(self):
        engine = MagicMock()
        connection = engine.connect.return_value.__enter__.return_value
        initialise_api_views(engine)

        connection.execute.assert_has_calls([
            call("DROP VIEW IF EXISTS public.view1name CASCADE"),
            call("DROP VIEW IF EXISTS legacy.view1name CASCADE"),
            call("CREATE VIEW legacy.view1name AS view1query"),
            call("DROP VIEW IF EXISTS public.view2name CASCADE"),
            call("DROP VIEW IF EXISTS legacy.view2name CASCADE"),
            call("CREATE VIEW legacy.view2name AS view2query"),
            call("DROP VIEW IF EXISTS public.view3name CASCADE"),
            call("DROP VIEW IF EXISTS legacy.view3name CASCADE"),
            call("CREATE VIEW legacy.view3name AS view3query"),
        ])
