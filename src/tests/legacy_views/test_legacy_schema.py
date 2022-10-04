"""This file tests the contents of the legacy views."""

import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobcore.typesystem.json import GobTypeJSONEncoder
from gobcore.views import GOBViews

from gobapi import gob_model
from gobapi.api import get_app
from gobapi.storage import connect, exec_statement


class TestLegacySchema(TestCase):

    def test_legacy_schema(self):
        """Tests views in legacy schema.

        To extend, just add a new expected view result as JSON in the expected_legacy_schema directory
        """
        connect()

        expected_files = Path(__file__).parent.joinpath('expected_legacy_schema').glob('*.json')

        for file in expected_files:
            tablename = file.stem
            with open(file, 'r') as f:
                expected = json.load(f)

                exec_result = exec_statement(f"SELECT * FROM legacy.{tablename} ORDER BY _gobid")

                # Encoding result to json first using GOBTypeJSONEncoder before decoding again, so that
                # Postgres types are cast correctly.
                transformed_result = json.loads(
                    json.dumps([dict(row) for row in exec_result], cls=GobTypeJSONEncoder))
                self.assertEqual(
                    expected, transformed_result,
                    f"Data in legacy schema does not match expected data for {tablename}")

    def test_materialized_views(self):
        connect()

        for collection_name in gob_model['rel']['collections']:
            tablename = gob_model.get_table_name('rel', collection_name)
            exec_statement(f"SELECT * FROM legacy.{tablename} LIMIT 1")

            mv_name = tablename.replace("rel_", "mv_", 1)
            exec_statement(f"SELECT * FROM legacy.{mv_name} LIMIT 1")


@patch("gobapi.api.AuditLogMiddleware", MagicMock())
class TestAPI(TestCase):
    graphql_query = """
query napPeilmerken {
  napPeilmerken {
    edges {
      node{
        identificatie
        ligtInBouwblok {
          edges {
            node{
              bronwaarde
            }
          }
        }
        status
        merk
        hoogteTovNap
      }
    }
  }
}"""

    def get_client(self):
        return get_app().test_client()

    def test_rest_api(self):
        """Simple test for REST API, making sure that legacy schema is used.

        To test contents of legacy schema, use test_legacy_schema above. No need to implement
        this one for every collection.
        """
        res = self.get_client().get('/gob/public/nap/peilmerken/')

        expected = {
            '_links': {
                'next': {
                    'href': None
                },
                'previous': {
                    'href': None
                },
                'self': {
                    'href': '/gob/public/nap/peilmerken/'
                }
            },
            'totalCount': 2,
            'pageSize': 100,
            'pages': 1,
            'results': [{
                'identificatie': '10780001',
                'hoogteTovNap': 2.927,
                'jaar': 2000,
                'merk': {
                    'code': '0',
                    'omschrijving': 'Ronde bout met opschrift NAP'
                },
                'omschrijving': 'Kantoor "Werkspoor" aan de Oostenburgervoorstraat (x=rechter dag van het linker kelderraam y=granieten plint)',
                'windrichting': 'NW',
                'xCoordinaatMuurvlak': 82.0,
                'yCoordinaatMuurvlak': 12.0,
                'rwsNummer': None,
                'geometrie': {
                    'type': 'Point',
                    'coordinates': [123520.0, 487010.0]
                },
                'status': {
                    'code': 3,
                    'omschrijving': 'Vervallen'
                },
                'vervaldatum': '2008-07-08',
                'publiceerbaar': True,
                '_links': {
                    'self': {
                        'href': '/gob/public/nap/peilmerken/10780001/'
                    }
                },
                '_embedded': {
                    'ligtInBouwblok': []
                }
            },
                {
                    'identificatie': '10580007',
                    'hoogteTovNap': 3.6852,
                    'jaar': 2000,
                    'merk': {
                        'code': '1',
                        'omschrijving': 'Ronde bout of althans aan de bovenzijde ronde bout zonder opschrift of met opschrift anders dan NAP'
                    },
                    'omschrijving': 'Oudeschans 2 (Noordwest gevel van de "Montelbaanstoren")',
                    'windrichting': 'N',
                    'xCoordinaatMuurvlak': 275.0,
                    'yCoordinaatMuurvlak': 96.0,
                    'rwsNummer': '25G0148',
                    'geometrie': {
                        'type': 'Point',
                        'coordinates': [122206.9, 487243.6]
                    },
                    'status': {
                        'code': 3,
                        'omschrijving': 'Vervallen'
                    },
                    'vervaldatum': '2018-05-03',
                    'publiceerbaar': True,
                    '_links': {
                        'self': {
                            'href': '/gob/public/nap/peilmerken/10580007/'
                        }
                    },
                    '_embedded': {
                        'ligtInBouwblok': []
                    }
                }]
        }

        self.assertEqual(res.json, expected)

    def test_graphql_api(self):
        """Simple test for GraphQL API, making sure that legacy schema is used.

        To test contents of legacy schema, use test_legacy_schema above. No need to implement
        this one for every collection.
        """

        res = self.get_client().post('/gob/public/graphql/', json={
            'query': self.graphql_query
        })

        expected = {
            'data': {
                'napPeilmerken': {
                    'edges': [{
                        'node': {
                            'identificatie': '10580007',
                            'ligtInBouwblok': {
                                'edges': [{
                                    'node': {
                                        'bronwaarde': None
                                    }
                                }]
                            },
                            'status': {
                                'code': 3,
                                'omschrijving': 'Vervallen'
                            },
                            'merk': {
                                'code': '1',
                                'omschrijving': 'Ronde bout of althans aan de bovenzijde ronde bout zonder opschrift of met opschrift anders dan NAP'
                            },
                            'hoogteTovNap': 3.6852
                        }
                    }, {
                        'node': {
                            'identificatie': '10780001',
                            'ligtInBouwblok': {
                                'edges': [{
                                    'node': {
                                        'bronwaarde': None
                                    }
                                }]
                            },
                            'status': {
                                'code': 3,
                                'omschrijving': 'Vervallen'
                            },
                            'merk': {
                                'code': '0',
                                'omschrijving': 'Ronde bout met opschrift NAP'
                            },
                            'hoogteTovNap': 2.927
                        }
                    }]
                }
            }
        }

        self.assertEqual(res.json, expected)

    def test_graphql_streaming_api(self):
        """Simple test for GraphQL Streaming API, making sure that legacy schema is used.
        To test contents of legacy schema, use test_legacy_schema above. No need to implement this one for every
        collection.
        """

        res = self.get_client().post('/gob/public/graphql/streaming/', json={
            'query': self.graphql_query
        })

        expected = """\
{"node": {"identificatie": "10580007", "status": {"code": 3, "omschrijving": "Vervallen"}, "merk": {"code": "1", "omschrijving": "Ronde bout of althans aan de bovenzijde ronde bout zonder opschrift of met opschrift anders dan NAP"}, "hoogteTovNap": 3.6852, "ligtInBouwblok": {"edges": []}}}
{"node": {"identificatie": "10780001", "status": {"code": 3, "omschrijving": "Vervallen"}, "merk": {"code": "0", "omschrijving": "Ronde bout met opschrift NAP"}, "hoogteTovNap": 2.927, "ligtInBouwblok": {"edges": []}}}

"""

        result = res.data.decode('utf-8')
        self.assertEqual(expected, result)

    @patch("gobapi.auth.auth_query.Authority.allows_access")
    def test_enhanced_views(self, mock_allows_access):
        """Tests that all existing enhanced view still work on the legacy schema
        Bypasses security
        """
        mock_allows_access.return_value = True
        client = self.get_client()

        views = GOBViews()
        for catalog in views.get_catalogs():
            for entity in views.get_entities(catalog):
                for view_name in views.get_views(catalog, entity):
                    res = client.get(f'/gob/public/{catalog}/{entity}/?view={view_name}')
                    self.assertEqual(200, res.status_code)
