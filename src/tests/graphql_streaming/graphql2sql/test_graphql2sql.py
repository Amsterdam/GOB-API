import re

from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from gobapi.graphql_streaming.graphql2sql.graphql2sql import GraphQL2SQL, GraphQLVisitor, GraphQLParser
from gobapi.graphql_streaming.graphql2sql.graphql2sql import NoAccessException, InvalidQueryException
from gobapi.graphql_streaming.utils import to_snake


class MockModel:
    data = {
        'catalog': {
            'collections': {
                'collectiona': {
                    'abbreviation': 'cola',
                    'has_states': False,
                    'attributes': {
                        'identificatie': {
                            'type': 'GOB.String',
                        },
                        'some_nested_relation': {
                            'type': 'GOB.Reference',
                            'ref': 'catalog:collectionb',
                        },
                        'some_nested_many_relation': {
                            'type': 'GOB.ManyReference',
                            'ref': 'catalog:collectionb',
                        }
                    },
                    'all_fields': [],
                },
                'collectionb': {
                    'abbreviation': 'colb',
                    'has_states': True,
                    'attributes': {
                        'identificatie': {
                            'type': 'GOB.String',
                        }
                    },
                    'all_fields': [],
                },
                'collectionc': {
                    'abbreviation': 'colc',
                    'has_states': True,
                    'attributes': {
                        'relation_to_b': {
                            'type': 'GOB.Reference',
                            'ref': 'catalog:collectionb',
                        },
                    },
                    'all_fields': [],
                },
                'collectionwithgeometry': {
                    'abbreviation': 'geocoll',
                    'has_states': False,
                    'attributes': {
                        'geofield': {
                            'type': 'GOB.Geo.Polygon'
                        }
                    },
                    'all_fields': [],
                }
            }
        }
    }

    def __getitem__(self, catalog_name):
        return self.data[catalog_name]

    def get_table_name(self, catalog_name: str, collection_name: str):
        return f"{catalog_name}_{collection_name}".lower()

    def get_catalog_collection_names_from_ref(self, ref: str):
        split = ref.split(':')
        return split[0], split[1]


@patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.gob_model", new_callable=MockModel)
@patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.get_relation_name",
       lambda m, cat, col, attr: f"{cat}_{col}_{attr}")
class TestGraphQL2SQL(TestCase):
    """Tests the GraphQL2SQL functionality as a whole.

    Includes large parts of GraphQLVisitor, SqlGenerator and GraphQL2SQL.

    Validates input GraphQL query with expected output SQL.
    """

    test_cases = [
        (
            '''
{
  catalogCollectiona {
    edges {
      node {
        identificatie
      }
    }
  }
}
''', '''
SELECT cola_0._gobid, cola_0.identificatie, 'catalog' AS _catalog, 'collectiona' AS _collection
FROM (
    SELECT * FROM legacy.catalog_collectiona
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _date_deleted IS NULL
    ORDER BY _gobid
) cola_0
ORDER BY cola_0._gobid
'''
        ),
        (
            '''
{
  catalogCollectiona(after: 2) {
    edges {
      node {
        identificatie
        cursor
      }
    }
  }
}
''', '''
    SELECT cola_0._gobid, cola_0.identificatie, cola_0._gobid AS cursor, 'catalog' AS _catalog, 'collectiona' AS _collection
    FROM (
        SELECT * FROM legacy.catalog_collectiona
        WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _gobid > 2 AND _date_deleted IS NULL
        ORDER BY _gobid
    ) cola_0
    ORDER BY cola_0._gobid
    '''
        ),
        (
            '''
{
  catalogCollectionwithgeometry {
    edges {
      node {
        identificatie
        geofield
      }
    }
  }
}
''', '''
SELECT geocoll_0._gobid, geocoll_0.identificatie, ST_AsText(geocoll_0.geofield) AS geofield, 'catalog' AS _catalog, 'collectionwithgeometry' AS _collection
FROM (
    SELECT * FROM legacy.catalog_collectionwithgeometry
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _date_deleted IS NULL
    ORDER BY _gobid
) geocoll_0
ORDER BY geocoll_0._gobid
'''
        ),
        (
            '''
{
  catalogCollectiona(filterarg: 3, filterarg2: "strval") {
    edges {
      node {
        identificatie
      }
    }
  }
}
''', '''
SELECT cola_0._gobid, cola_0.identificatie, 'catalog' AS _catalog, 'collectiona' AS _collection
FROM (
    SELECT * FROM legacy.catalog_collectiona
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
    AND filterarg = 3 AND filterarg2 = 'strval' AND _date_deleted IS NULL
    ORDER BY _gobid
) cola_0
ORDER BY cola_0._gobid
'''
        ),
        (
            '''
{
  catalogCollectiona(first: 20) {
    edges {
      node {
        identificatie
      }
    }
  }
}
''', '''
SELECT cola_0._gobid, cola_0.identificatie, 'catalog' AS _catalog, 'collectiona' AS _collection
FROM (
    SELECT * FROM legacy.catalog_collectiona
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _date_deleted IS NULL
    ORDER BY _gobid
    LIMIT 20
) cola_0
ORDER BY cola_0._gobid
'''
        ),
        (
            '''
{
  catalogCollectiona(active: false) {
    edges {
      node {
        identificatie
      }
    }
  }
}
''', '''
SELECT cola_0._gobid, cola_0.identificatie, 'catalog' AS _catalog, 'collectiona' AS _collection
FROM (
    SELECT * FROM legacy.catalog_collectiona
    WHERE _date_deleted IS NULL
    ORDER BY _gobid
) cola_0
ORDER BY cola_0._gobid
'''),
        (

            '''
{
  catalogCollectiona(active: false) {
    edges {
      node {
        identificatie

        someNestedRelation(someProperty: "someval") {
            edges {
                node {
                    nestedIdentificatie
                    bronwaarde
                    broninfo
                    beginGeldigheidRelatie
                    eindGeldigheidRelatie
                }
            }
        }
      }
    }
  }
}''',
        # bronwaarde and broninfo are added as special case, they change the query by adding the _src selection
        # Same goes for beginGeldigheidRelatie and eindGeldigheidRelatie, they should be added to the reference
            '''
SELECT
cola_0._gobid,
cola_0.identificatie,
'catalog' AS _catalog,
'collectiona' AS _collection,
cola_0.some_nested_relation AS _src_some_nested_relation,
json_build_object('_gobid', colb_0._gobid,'nested_identificatie', colb_0.nested_identificatie,
 'begin_geldigheid_relatie', rel_0.begin_geldigheid,'eind_geldigheid_relatie', rel_0.eind_geldigheid,
 '_catalog', 'catalog', '_collection', 'collectionb') AS _some_nested_relation
FROM (
    SELECT *
    FROM legacy.catalog_collectiona
    WHERE _date_deleted IS NULL
    ORDER BY _gobid

) cola_0
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_relation rel_0 ON rel_0.src_id = cola_0._id AND rel_0.bronwaarde = cola_0.some_nested_relation->>'bronwaarde'
LEFT JOIN legacy.catalog_collectionb colb_0 ON rel_0.dst_id = colb_0._id AND rel_0.dst_volgnummer = colb_0.volgnummer AND (colb_0.some_property = 'someval')
AND (COALESCE(colb_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY cola_0._gobid
         '''

        ),
        (
            '''
{
  catalogCollectionc(active: false) {
    edges {
      node {
        identificatie

        relationToB(someProperty: "someval") {
            edges {
                node {
                    nestedIdentificatie
                    bronwaarde
                    broninfo
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
colc_0._gobid,
colc_0.identificatie,
'catalog' AS _catalog,
'collectionc' AS _collection,
colc_0.relation_to_b AS _src_relation_to_b,
json_build_object('_gobid', colb_0._gobid,'nested_identificatie', colb_0.nested_identificatie,
 '_catalog', 'catalog', '_collection', 'collectionb') AS _relation_to_b
FROM (
    SELECT *
    FROM legacy.catalog_collectionc
    WHERE _date_deleted IS NULL
    ORDER BY _gobid

) colc_0
LEFT JOIN legacy.mv_catalog_collectionc_relation_to_b rel_0
ON rel_0.src_id = colc_0._id
AND rel_0.bronwaarde = colc_0.relation_to_b->>'bronwaarde' AND rel_0.src_volgnummer = colc_0.volgnummer
LEFT JOIN legacy.catalog_collectionb colb_0
ON rel_0.dst_id = colb_0._id AND rel_0.dst_volgnummer = colb_0.volgnummer AND (colb_0.some_property = 'someval')
AND (COALESCE(colb_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY colc_0._gobid
         '''

        ),
        (
            '''
{
  catalogCollectionb(active: false) {
    edges {
      node {
        identificatie

        invRelationToBCatalogCollectionc(someProperty: "someval") {
            edges {
                node {
                    nestedIdentificatie
                    bronwaarde
                    broninfo
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
colb_0._gobid,
colb_0.identificatie,
'catalog' AS _catalog,
'collectionb' AS _collection,
json_build_object('_gobid', colc_0._gobid,'nested_identificatie',
    colc_0.nested_identificatie, '_catalog', 'catalog', '_collection', 'collectionc') AS _inv_relation_to_b_catalog_collectionc
FROM (
    SELECT *
    FROM legacy.catalog_collectionb
    WHERE _date_deleted IS NULL
    ORDER BY _gobid

) colb_0
LEFT JOIN legacy.mv_catalog_collectionc_relation_to_b rel_0
ON rel_0.dst_id = colb_0._id AND rel_0.dst_volgnummer = colb_0.volgnummer
LEFT JOIN legacy.catalog_collectionc colc_0
ON rel_0.src_id = colc_0._id AND rel_0.src_volgnummer = colc_0.volgnummer AND (colc_0.some_property = 'someval')
AND (COALESCE(colc_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY colb_0._gobid
         '''

        ),
        (
            '''
{
  catalogCollectiona(active: false) {
    edges {
      node {
        identificatie

        someNestedManyRelation(filterArg: "filterval") {
            edges {
                node {
                    nestedIdentificatie
                    bronwaarde
                    broninfo
                }
            }
        }
      }
    }
  }
}''',
            # bronwaarde and broninfo are added as special case, they change the query by adding the _src selection
            '''
SELECT
cola_0._gobid,
cola_0.identificatie,
'catalog' AS _catalog,
'collectiona' AS _collection,
rel_bw_0.item AS _src_some_nested_many_relation,
json_build_object('_gobid', colb_0._gobid,'nested_identificatie',
colb_0.nested_identificatie, '_catalog', 'catalog', '_collection', 'collectionb') AS _some_nested_many_relation
FROM (
    SELECT *
    FROM legacy.catalog_collectiona
    WHERE _date_deleted IS NULL
    ORDER BY _gobid

) cola_0
LEFT JOIN jsonb_array_elements(cola_0.some_nested_many_relation) rel_bw_0(item)
ON rel_bw_0.item->>'bronwaarde' IS NOT NULL
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_many_relation rel_0
ON rel_0.src_id = cola_0._id AND rel_0.bronwaarde = rel_bw_0.item->>'bronwaarde'
LEFT JOIN legacy.catalog_collectionb colb_0
ON rel_0.dst_id = colb_0._id AND rel_0.dst_volgnummer = colb_0.volgnummer AND (colb_0.filter_arg = 'filterval')
AND (COALESCE(colb_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY cola_0._gobid
         '''
        ),
        (
            '''
{
  catalogCollectionb {
    edges {
      node {
        identificatie

        invSomeNestedManyRelationCatalogCollectiona(someProperty: "someval") {
            edges {
                node {
                   identificatie
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
colb_0._gobid,
colb_0.identificatie,
'catalog' AS _catalog,
'collectionb' AS _collection,
json_build_object('_gobid',
cola_0._gobid,'identificatie', cola_0.identificatie, '_catalog', 'catalog', '_collection', 'collectiona') AS _inv_some_nested_many_relation_catalog_collectiona
FROM (
    SELECT *
    FROM legacy.catalog_collectionb
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _date_deleted IS NULL
    ORDER BY _gobid

) colb_0
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_many_relation rel_0
ON rel_0.dst_id = colb_0._id AND rel_0.dst_volgnummer = colb_0.volgnummer
LEFT JOIN legacy.catalog_collectiona cola_0 ON rel_0.src_id = cola_0._id AND (cola_0.some_property = 'someval')
AND (COALESCE(cola_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY colb_0._gobid
         '''
        ),
        (
            '''
{
  catalogCollectionb {
    edges {
      node {
        identificatie

        invSomeNestedRelationCatalogCollectiona(someProperty: "someval") {
            edges {
                node {
                   identificatie
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
colb_0._gobid,
colb_0.identificatie,
'catalog' AS _catalog,
'collectionb' AS _collection,
json_build_object('_gobid', cola_0._gobid,'identificatie',
cola_0.identificatie, '_catalog', 'catalog', '_collection', 'collectiona') AS _inv_some_nested_relation_catalog_collectiona
FROM (
    SELECT *
    FROM legacy.catalog_collectionb
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _date_deleted IS NULL
    ORDER BY _gobid

) colb_0
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_relation rel_0
ON rel_0.dst_id = colb_0._id AND rel_0.dst_volgnummer = colb_0.volgnummer
LEFT JOIN legacy.catalog_collectiona cola_0 ON rel_0.src_id = cola_0._id AND (cola_0.some_property = 'someval')
AND (COALESCE(cola_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY colb_0._gobid
         '''
        ),
        (

            '''
{
  catalogCollectiona(active: false) {
    edges {
      node {
        identificatie

        relationAlias: someNestedRelation(someProperty: "someval") {
            edges {
                node {
                    nestedIdentificatie
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
cola_0._gobid,
cola_0.identificatie,
'catalog' AS _catalog,
'collectiona' AS _collection,
json_build_object('_gobid', colb_0._gobid,'nested_identificatie', colb_0.nested_identificatie, '_catalog', 'catalog', '_collection', 'collectionb') AS _relation_alias
FROM (
    SELECT *
    FROM legacy.catalog_collectiona
    WHERE _date_deleted IS NULL
    ORDER BY _gobid

) cola_0
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_relation rel_0
ON rel_0.src_id = cola_0._id
LEFT JOIN legacy.catalog_collectionb colb_0 ON rel_0.dst_id = colb_0._id
AND rel_0.dst_volgnummer = colb_0.volgnummer AND (colb_0.some_property = 'someval')
AND (COALESCE(colb_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY cola_0._gobid
         '''
        ),
        (

            '''
{
  catalogCollectiona(active: false) {
    edges {
      node {
        identificatie

        relationAlias: someNestedRelation(first: 2) {
            edges {
                node {
                    nestedIdentificatie
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
cola_0._gobid,
cola_0.identificatie,
'catalog' AS _catalog,
'collectiona' AS _collection,
json_build_object('_gobid', colb_0._gobid,'nested_identificatie',
colb_0.nested_identificatie, '_catalog', 'catalog', '_collection', 'collectionb') AS _relation_alias
FROM (
    SELECT *
    FROM legacy.catalog_collectiona
    WHERE _date_deleted IS NULL
    ORDER BY _gobid

) cola_0
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_relation rel_0
ON rel_0._gobid IN (
    SELECT _gobid FROM legacy.mv_catalog_collectiona_some_nested_relation rel
    WHERE rel.src_id = cola_0._id
    LIMIT 2
)
LEFT JOIN legacy.catalog_collectionb colb_0 ON rel_0.dst_id = colb_0._id
AND rel_0.dst_volgnummer = colb_0.volgnummer
AND (COALESCE(colb_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY cola_0._gobid
         '''
        ),
        (
            '''
{
  catalogCollectionb {
    edges {
      node {
        identificatie

        invSomeNestedRelationCatalogCollectiona(first: 1, someProperty: "someval") {
            edges {
                node {
                   identificatie
                }
            }
        }
      }
    }
  }
}''',
            '''
SELECT
colb_0._gobid,
colb_0.identificatie,
'catalog' AS _catalog,
'collectionb' AS _collection,
json_build_object('_gobid', cola_0._gobid,'identificatie',
cola_0.identificatie, '_catalog', 'catalog', '_collection', 'collectiona') AS _inv_some_nested_relation_catalog_collectiona
FROM (
    SELECT *
    FROM legacy.catalog_collectionb
    WHERE (COALESCE(_expiration_date, '9999-12-31'::timestamp without time zone) > NOW()) AND _date_deleted IS NULL
    ORDER BY _gobid

) colb_0
LEFT JOIN legacy.mv_catalog_collectiona_some_nested_relation rel_0 ON rel_0._gobid IN (
    SELECT _gobid FROM legacy.mv_catalog_collectiona_some_nested_relation rel
    WHERE rel.dst_id = colb_0._id AND rel.dst_volgnummer = colb_0.volgnummer
    LIMIT 1
)
LEFT JOIN legacy.catalog_collectiona cola_0 ON rel_0.src_id = cola_0._id AND (cola_0.some_property = 'someval')
AND (COALESCE(cola_0._expiration_date, '9999-12-31'::timestamp without time zone) > NOW())
ORDER BY colb_0._gobid
         '''
        ),

    ]

    def normalise_whitespace(self, string: str):
        whitespacechars = re.sub(r'([,(,)])', ' g<1> ', string)
        return re.sub(r'\s+', ' ', whitespacechars).strip()

    def assert_result(self, in_put, expected_result, result):
        expect = self.normalise_whitespace(expected_result)
        actual = self.normalise_whitespace(result)
        if expect != actual:
            # These lines help to resolve test errors...
            print("FAILURE!")
            print(f"INPUT:{in_put}")
            print(f"OUTPUT:\n{result}")
        self.assertEqual(expect, actual)

    @patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.SqlGenerator._validate_attribute", MagicMock())
    @patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.resolve_schema_collection_name")
    def test_graphql2sql(self, mock_resolve, mock_model):
        mock_resolve.side_effect = lambda n : to_snake(n).split('_')

        for inp, outp in self.test_cases:
            graphql2sql = GraphQL2SQL(inp)
            # _validate_attribute of SqlGenerator is mocked to avoid having to define all fields
            self.assert_result(inp, outp, graphql2sql.sql())

    @patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.SqlGenerator._validate_attribute", MagicMock())
    @patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.resolve_schema_collection_name")
    @patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.Authority")
    def test_graphql2sql_no_access(self, mock_authority, mock_resolve, mock_model):
        mock_authority.return_value.allows_access.return_value = False
        mock_resolve.side_effect = lambda n : to_snake(n).split('_')

        with self.assertRaises(NoAccessException):
            inp, outp = self.test_cases[0]
            graphql2sql = GraphQL2SQL(inp)
            self.assert_result(inp, outp, graphql2sql.sql())

    @patch("gobapi.graphql_streaming.graphql2sql.graphql2sql.resolve_schema_collection_name",
            lambda n : to_snake(n).split('_'))
    def test_invalid_attributes(self, mock_model):
        query = """
{
  catalogCollectionc(active: false) {
    edges {
      node {
        identificatie

        relationToB(someProperty: "someval") {
            edges {
                node {
                    nestedIdentificatie
                    bronwaarde
                    broninfo
                }
            }
        }
      }
    }
  }
}"""
        query2 = """
{
  catalogCollectionb(active: false) {
    edges {
      node {
        identificatie

        invRelationToBCatalogCollectionc(someProperty: "someval") {
            edges {
                node {
                    nestedIdentificatie
                    bronwaarde
                    broninfo
                }
            }
        }
      }
    }
  }
}"""

        def setup_model():
            mock_model.data['catalog']['collections']['collectionc']['all_fields'] = [
                '_gobid', 'identificatie', 'nested_identificatie', 'relation_to_b']
            mock_model.data['catalog']['collections']['collectionb']['all_fields'] = [
                '_gobid', 'identificatie', 'nested_identificatie']

        def run_query(q):
            graphql2sql = GraphQL2SQL(q)
            graphql2sql.sql()

        def delete_field(collection: str, field: str):
            idx = mock_model.data['catalog']['collections'][collection]['all_fields'].index(field)
            del mock_model.data['catalog']['collections'][collection]['all_fields'][idx]

        # Should both succeed
        setup_model()
        run_query(query)
        run_query(query2)

        # Now remove 'identificatie' from both collections
        setup_model()
        delete_field('collectionb', 'identificatie')
        delete_field('collectionc', 'identificatie')

        with self.assertRaisesRegex(
                InvalidQueryException, "Attribute identificatie does not exist for collectionc"):
            run_query(query)
        with self.assertRaisesRegex(
                InvalidQueryException, "Attribute identificatie does not exist for collectionb"):
            run_query(query2)

        # Remove relation_to_b
        setup_model()
        delete_field('collectionc', 'relation_to_b')

        with self.assertRaisesRegex(
                InvalidQueryException, "Attribute relation_to_b does not exist for catalogCollectionc"):
            run_query(query)
        with self.assertRaisesRegex(
                InvalidQueryException, "Attribute relation_to_b does not exist for collectionc"):
            run_query(query2)

        # Remove nested identificatie
        setup_model()
        delete_field('collectionb', 'nested_identificatie')
        delete_field('collectionc', 'nested_identificatie')

        with self.assertRaisesRegex(
                InvalidQueryException, "Attribute nestedIdentificatie does not exist for relationToB"):
            run_query(query)
        with self.assertRaisesRegex(
                InvalidQueryException, "Attribute nestedIdentificatie does not exist for invRelationToBCatalogCollectionc"):
            run_query(query2)

    def test_invalid_relation(self, mock_model):
        query = """
        {
          catalogCollectionc(active: false) {
            edges {
              node {
                identificatie

                relationToB(someProperty: "someval") {
                    edges {
                        node {
                            nestedIdentificatie
                            bronwaarde
                            broninfo
                        }
                    }
                }
              }
            }
          }
        }"""

        with self.assertRaisesRegex(InvalidQueryException, "catalogCollectionc is not a valid entity"):
            graphql2sql = GraphQL2SQL(query)
            graphql2sql.sql()


class TestGraphQLVisitor(TestCase):

    def setUp(self) -> None:
        self.visitor = GraphQLVisitor()

    def test_visitAlias(self):
        arg = MagicMock()
        self.visitor.visitAlias(arg)
        arg.NAME.assert_has_calls([call(1), call().getText(), call(0), call().getText()])

    def test_visitFieldName(self):
        self.visitor.visitAlias = MagicMock()
        arg = MagicMock()
        arg.alias.return_value = MagicMock()

        self.visitor.visitFieldName(arg)
        self.visitor.visitAlias.assert_called_with(arg.alias.return_value)

    def test_visitBooleanValue(self):
        arg = MagicMock()
        arg.BOOLEAN.return_value = 'false'

        self.assertFalse(self.visitor.visitBooleanValue(arg))

        arg.BOOLEAN.return_value = 'true'
        self.assertTrue(self.visitor.visitBooleanValue(arg))

    def test_visitNumberValue(self):
        arg = MagicMock()
        arg.NUMBER.return_value = 248042
        self.assertEqual(str(arg.NUMBER.return_value), self.visitor.visitNumberValue(arg))

    def test_visitStringValue(self):
        arg = MagicMock()
        arg.STRING.return_value = 'somestringvalue'
        self.assertEqual(arg.STRING.return_value, self.visitor.visitStringValue(arg))

    def test_visitField_ignore_page_info(self):
        arg = MagicMock()
        arg.selectionSet.return_value = True
        arg.directives.return_value = False
        self.visitor.visitSelectionSet = MagicMock()
        self.visitor.visitFieldName = MagicMock(return_value=('pageInfo', 'pageInfo'))
        self.visitor.visitField(arg)
        self.visitor.visitSelectionSet.assert_not_called()

    def test_visitValueOrVariable(self):
        cases = [
            (GraphQLParser.StringValueContext, 'visitStringValue'),
            (GraphQLParser.NumberValueContext, 'visitNumberValue'),
            (GraphQLParser.BooleanValueContext, 'visitBooleanValue'),
        ]

        for context, callmethod in cases:
            arg = MagicMock()
            arg.value.return_value = context(MagicMock(), MagicMock())
            mock_visit_value = MagicMock()
            self.visitor.__setattr__(callmethod, mock_visit_value)

            res = self.visitor.visitValueOrVariable(arg)
            mock_visit_value.assert_called_with(arg.value.return_value)
            self.assertEqual(mock_visit_value.return_value, res)

        # Test not implemented value type
        arg = MagicMock()
        arg.value.return_value = 'some other value'

        with self.assertRaises(NotImplementedError):
            self.visitor.visitValueOrVariable(arg)

        # Test no value
        arg = MagicMock()
        arg.value.return_value = False
        self.visitor.visitVariable = MagicMock()
        self.visitor.visitValueOrVariable(arg)
        self.visitor.visitVariable.assert_called_with(arg.variable.return_value)
