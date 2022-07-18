from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from gobapi.legacy_views.create import create_legacy_views


class MockModel:

    def get_catalogs(self):
        return {
            'gebieden': {

            },
            'nap': {

            },
            'rel': {

            }
        }

    def get_collections(self, catalog_name):
        return {
            'gebieden': {
                'buurten': {},
                'bouwblokken': {},
            },
            'nap': {
                'peilmerken': {
                    'all_fields': {
                        # Bogus fields, plus the fields from the definition
                        '_id': {},
                        'ligt_in_bouwblok': {},
                        'merk': {},
                        'status': {},
                        'not_overridden_field': {}
                    }
                },
            },
            'rel': {
                'nap_pmk_gbd_bbk_ligt_in_bouwblok': {
                    'all_fields': {
                        # Bogus fields, not important
                        '_id': {},
                        'a': {},
                        'b': {}
                    }
                }
            }
        }[catalog_name]

    def get_collection(self, catalog_name, collection_name):
        return self.get_collections(catalog_name)[collection_name]

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

        # This tests override two queries; nap peilmerken and rel nap_pmk_gbd_bbk_ligt_in_bouwblok
        # Nap peilmerken overrides columns, rel nap_pmk_gbd_bbk_ligt_in_bouwblok overrides the name
        # Uses the real view_definitions in this repo, no mocks.
        expected_nap_peilmerken_query = """SELECT
  _id,
  ligt_in_gebieden_bouwblok as ligt_in_bouwblok,
  jsonb_build_object(
  'code', merk_code,
  'omschrijving', merk_omschrijving
)
 as merk,
  jsonb_build_object(
  'code', status_code,
  'omschrijving', status_omschrijving
)
 as status,
  not_overridden_field
FROM public.nap_peilmerken"""

        expected_rel_query = """SELECT
  _id,
  a,
  b
FROM public.rel_nap_pmk_gbd_bbk_ligt_in_gebieden_bouwblok"""

        connection.__enter__.return_value.execute.assert_has_calls([
            call("CREATE SCHEMA IF NOT EXISTS legacy"),
            call("CREATE OR REPLACE VIEW legacy.gebieden_buurten AS SELECT * FROM public.gebieden_buurten"),
            call("CREATE OR REPLACE VIEW legacy.gebieden_bouwblokken AS SELECT * FROM public.gebieden_bouwblokken"),
            call(f"CREATE OR REPLACE VIEW legacy.nap_peilmerken AS {expected_nap_peilmerken_query}"),
            call(f"CREATE OR REPLACE VIEW legacy.rel_nap_pmk_gbd_bbk_ligt_in_bouwblok AS {expected_rel_query}"),
            call("CREATE OR REPLACE VIEW legacy.mv_gbd_brt_abc_abc AS SELECT * FROM public.mv_gbd_brt_abc_abc"),
            call("CREATE OR REPLACE VIEW legacy.mv_gbd_brt_def_def AS SELECT * FROM public.mv_gbd_brt_def_def"),
            call("CREATE OR REPLACE VIEW legacy.spatial_ref_sys AS SELECT * FROM public.spatial_ref_sys"),
            call("CREATE OR REPLACE VIEW legacy.alembic_version AS SELECT * FROM public.alembic_version"),
            call("CREATE OR REPLACE VIEW legacy.events AS SELECT * FROM public.events"),
        ])
