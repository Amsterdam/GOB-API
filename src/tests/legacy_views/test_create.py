from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from psycopg2.errors import InvalidTableDefinition
from sqlalchemy.exc import ProgrammingError

from gobapi.legacy_views.create import _create_view_with_drop_fallback, create_legacy_views


class MockModel:
    data = {
        'some_catalog': {
            'collections': {
                'some_collection': {},
                'some_other_collection': {},
            }
        },
        'nap': {
            'collections': {
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
            }
        },
        'rel': {
            'collections': {
                'nap_pmk_gbd_bbk_ligt_in_bouwblok': {
                    'all_fields': {
                        # Bogus fields, not important
                        '_id': {},
                        'a': {},
                        'b': {}
                    }
                },
                'mbn_mtg_mbn_rpt__rft_n__referentiepunten': {
                    'all_fields': {
                        # Will be the full fieldset in the non-mocked version
                        '_id': {}
                    }
                },
            }
        }
    }

    def __init__(self, data=None):
        if data:
            # Overwrite default
            self.data = data

    def __getitem__(self, catalog_name):
        return self.data[catalog_name]

    def items(self):
        return self.data.items()

    def get_table_name(self, catalog_name, collection_name):
        return f"{catalog_name}_{collection_name}"


class MockRelations:
    data = {
        'collections': {
            'gbd_brt_abc_abc': {},
            'gbd_brt_def_def': {},
            'nap_pmk_gbd_bbk_ligt_in_bouwblok': {},
            'mbn_mtg_mbn_rpt__rft_n__referentiepunten': {},
        }
    }

    def __init__(self, data=None):
        if data is not None:
            # Overwrite default
            self.data = data

    def get_relations(self, model):
        return self.data


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
            call("CREATE OR REPLACE VIEW legacy.some_catalog_some_collection AS SELECT * FROM public.some_catalog_some_collection"),
            call("CREATE OR REPLACE VIEW legacy.some_catalog_some_other_collection AS SELECT * FROM public.some_catalog_some_other_collection"),
            call(f"CREATE OR REPLACE VIEW legacy.nap_peilmerken AS {expected_nap_peilmerken_query}"),
            call(f"CREATE OR REPLACE VIEW legacy.rel_nap_pmk_gbd_bbk_ligt_in_bouwblok AS {expected_rel_query}"),
            call("CREATE OR REPLACE VIEW legacy.rel_mbn_mtg_mbn_rpt__rft_n__referentiepunten AS SELECT\n  _id\nFROM public.rel_mbn_mtg_mbn_rpt__rft_n__meetbouten_referentiepunten"),
            call("CREATE OR REPLACE VIEW legacy.mv_gbd_brt_abc_abc AS SELECT * FROM public.mv_gbd_brt_abc_abc"),
            call("CREATE OR REPLACE VIEW legacy.mv_gbd_brt_def_def AS SELECT * FROM public.mv_gbd_brt_def_def"),

            # With overridden tablename
            call("CREATE OR REPLACE VIEW legacy.mv_nap_pmk_gbd_bbk_ligt_in_bouwblok AS SELECT * FROM public.mv_nap_pmk_gbd_bbk_ligt_in_gebieden_bouwblok"),
            call("CREATE OR REPLACE VIEW legacy.mv_mbn_mtg_mbn_rpt__rft_n__referentiepunten AS SELECT * FROM public.mv_mbn_mtg_mbn_rpt__rft_n__meetbouten_referentiepunten"),
        ])

    @patch("gobapi.legacy_views.create.relations", MockRelations({"collections": {}}))
    def test_create_legacy_views_changed_definition(self):
        engine = MagicMock()
        connection = engine.connect.return_value
        execute = connection.__enter__.return_value.execute
        error = ProgrammingError("some statement", "params", InvalidTableDefinition())
        execute.side_effect = [None, error, None, None]

        model = MockModel({
            "some_catalog": {
                "collections": {
                    "some_collection": {}
                }
            }
        })
        create_legacy_views(model, engine)

        execute.assert_has_calls([
            call("CREATE SCHEMA IF NOT EXISTS legacy"),
            # This call fails on an InvalidTableDefinition ProgrammingError.
            call(
                "CREATE OR REPLACE VIEW legacy.some_catalog_some_collection AS SELECT * FROM public.some_catalog_some_collection"),
            # Then we drop the view
            call("DROP VIEW legacy.some_catalog_some_collection CASCADE"),
            # And try again
            call(
                "CREATE OR REPLACE VIEW legacy.some_catalog_some_collection AS SELECT * FROM public.some_catalog_some_collection")
        ])

    def test_create_view_with_drop_fallback_database_error(self):
        class SomeOtherException(Exception):
            pass

        connection = MagicMock()
        error = ProgrammingError("some statement", "params", SomeOtherException())
        connection.execute.side_effect = error

        with self.assertRaises(ProgrammingError):
            _create_view_with_drop_fallback("view name", "query", connection)
