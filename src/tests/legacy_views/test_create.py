from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from gobapi.legacy_views.create import create_legacy_views


class MockModel:

    def get_catalogs(self):
        return {
            'gebieden': {

            },
            'nap': {

            }
        }

    def get_collections(self, catalog_name):
        return {
            'gebieden': {
                'buurten': {},
                'bouwblokken': {},
            },
            'nap': {
                'peilmerken': {},
            }
        }[catalog_name]

    def get_table_name(self, catalog_name, collection_name):
        return f"{catalog_name}_{collection_name}"


class MockRelations:

    def get_relations(self, model):
        return {
            'collections': {
                'gbd_brt_abc_abc': {},
                'gbd_brt_def_def': {},
            }
        }


class TestLegacyViews(TestCase):

    @patch("gobapi.legacy_views.create.relations", MockRelations())
    def test_create_legacy_views(self):
        engine = MagicMock()
        connection = engine.connect.return_value

        create_legacy_views(MockModel(), engine)

        connection.__enter__.return_value.execute.assert_has_calls([
            call("CREATE SCHEMA IF NOT EXISTS legacy"),
            call("CREATE OR REPLACE VIEW legacy.gebieden_buurten AS SELECT * FROM public.gebieden_buurten"),
            call("CREATE OR REPLACE VIEW legacy.gebieden_bouwblokken AS SELECT * FROM public.gebieden_bouwblokken"),
            call("CREATE OR REPLACE VIEW legacy.nap_peilmerken AS SELECT * FROM public.nap_peilmerken"),
            call("CREATE OR REPLACE VIEW legacy.mv_gbd_brt_abc_abc AS SELECT * FROM public.mv_gbd_brt_abc_abc"),
            call("CREATE OR REPLACE VIEW legacy.mv_gbd_brt_def_def AS SELECT * FROM public.mv_gbd_brt_def_def"),
            call("CREATE OR REPLACE VIEW legacy.spatial_ref_sys AS SELECT * FROM public.spatial_ref_sys"),
            call("CREATE OR REPLACE VIEW legacy.alembic_version AS SELECT * FROM public.alembic_version"),
            call("CREATE OR REPLACE VIEW legacy.events AS SELECT * FROM public.events"),
        ])
