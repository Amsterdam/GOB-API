from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from gobapi.graphql_streaming.response import GraphQLStreamingResponseBuilder

from gobcore.exceptions import GOBException
from gobcore.model.metadata import FIELD, PUBLIC_META_FIELDS


class TestGraphQLStreamingResponseBuilder(TestCase):

    def get_instance(self, rows=['some', 'rows'], relations_hierarchy={'some': 'hierarchy'}, selections=None):
        self.rows = rows
        self.relations_hierarchy = relations_hierarchy
        self.selections = selections or {}
        self.instance = GraphQLStreamingResponseBuilder(rows, relations_hierarchy, self.selections)
        self.instance._resolver = MagicMock()
        return self.instance

    def test_init(self):
        builder = self.get_instance()

        self.assertEqual(self.rows, builder.rows)
        self.assertEqual(self.relations_hierarchy, builder.relations_hierarchy)
        self.assertIsNone(builder.last_id)

    def test_to_node(self):
        builder = self.get_instance()
        self.assertEqual({'node': {'some': 'object'}}, builder._to_node({'some': 'object'}))

    def test_relation_from_row(self):
        row = {
            '_rel_attribute': MagicMock(),
            '_other_rel_attribute': MagicMock(),
            '_very_long_rel_attribute_th': MagicMock(),  # Relation name shortened by the database
            'not_a_relation_attribute': MagicMock(),
        }

        testcases = [
            ('rel_attribute', row['_rel_attribute']),
            ('other_rel_attribute', row['_other_rel_attribute']),
            ('very_long_rel_attribute_that_could_be_shortened_by_the_database', row['_very_long_rel_attribute_th']),
        ]

        builder = self.get_instance()

        for relation_name, result_relation in testcases:
            self.assertEqual(result_relation, builder._relation_from_row(row, relation_name))

        with self.assertRaises(KeyError):
            # Regular attribute
            builder._relation_from_row(row, 'not_a_relation_attribute')

        with self.assertRaises(KeyError):
            builder._relation_from_row(row, 'non_existent_attribute')

    def test_add_sourcevalues_to_row(self):
        builder = self.get_instance()
        builder.requested_sourcevalues = {
            'relAtionA': [FIELD.SOURCE_VALUE],
            'relAtionB': [FIELD.SOURCE_INFO],
            'relAtionC': [FIELD.SOURCE_VALUE, FIELD.SOURCE_INFO],
            'relAtionD': [],
            'relAtionE': [FIELD.SOURCE_VALUE, FIELD.SOURCE_INFO],
            'relAtionF': [FIELD.SOURCE_VALUE, FIELD.SOURCE_INFO],
        }
        row = {
            '_srcRelAtionA': {
                FIELD.SOURCE_VALUE: 'svA',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'AA',
                }
            },
            '_srcRelAtionB': {
                FIELD.SOURCE_VALUE: 'svB',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'BB',
                }
            },
            '_srcRelAtionC': {
                FIELD.SOURCE_VALUE: 'svC',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'CC',
                }
            },
            '_srcRelAtionD': {
                FIELD.SOURCE_VALUE: 'svD',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'DD',
                }
            },
            '_srcRelAtionE': {
                FIELD.SOURCE_VALUE: 'svE',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'EE',
                }
            },
            '_srcRelAtionF': None,
            '_relAtionA': {
                'someField': 'AAA',
            },
            '_relAtionB': {
                'someField': 'BBB',
            },
            '_relAtionC': {
                'someField': 'CCC',
            },
            '_relAtionD': {
                'someField': 'DDD',
            },
            '_relAtionE': None,
            '_relAtionF': {
                'someField': 'FFF',
            }
        }
        builder._add_sourcevalues_to_row(row)

        self.assertEqual({
            '_relAtionA': {
                'someField': 'AAA',
                FIELD.SOURCE_VALUE: 'svA',
            },
            '_relAtionB': {
                'someField': 'BBB',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'BB',
                },
            },
            '_relAtionC': {
                'someField': 'CCC',
                FIELD.SOURCE_VALUE: 'svC',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'CC',
                }
            },
            '_relAtionD': {
                'someField': 'DDD',
            },
            '_relAtionE': {
                FIELD.SOURCE_VALUE: 'svE',
                FIELD.SOURCE_INFO: {
                    'someOtherField': 'EE',
                }
            },
            '_relAtionF': {
                'someField': 'FFF',
            }
        }, row)

    def test_add_row_to_entity_empty(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a', 'b']
        builder.root_relation = 'rootrel'
        builder.relations_hierarchy = {
            'a': 'rootrel',
            'b': 'a'
        }

        entity = {'existing': 'value'}
        row = {
            '_a': {'some': 'value'},
            '_b': {'some_other': 'value'},
        }

        expected_result = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            'some': 'value',
                            'b': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value'},
                                    }
                                ]
                            }
                        },
                    }
                ]
            },
        }

        builder._add_row_to_entity(row, entity)
        self.assertEqual(entity, expected_result)

    def test_add_row_to_entity_empty_nested_relation(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a', 'b']
        builder.root_relation = 'rootrel'
        builder.relations_hierarchy = {
            'a': 'rootrel',
            'b': 'a'
        }

        entity = {'existing': 'value'}
        row = {
            '_a': {'some': 'value'},
            '_b': None,
        }

        expected_result = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            'some': 'value',
                            'b': {
                                'edges': []
                            }
                        },
                    }
                ]
            },
        }

        builder._add_row_to_entity(row, entity)
        self.assertEqual(entity, expected_result)

    def test_add_row_to_entity_empty_relations(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a', 'b', 'c']
        builder.root_relation = 'rootrel'
        builder.relations_hierarchy = {
            'a': 'rootrel',
            'b': 'a',
            'c': 'b',
        }

        entity = {'existing': 'value'}
        row = {
            '_a': None,
            '_b': None,
            '_c': None,
        }

        expected_result = {
            'existing': 'value',
            'a': {
                'edges': []  # Shows empty list for top relation. Nested relations are - of course - not visible
            },
        }

        builder._add_row_to_entity(row, entity)
        self.assertEqual(entity, expected_result)

    def test_add_row_to_entity_add(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a', 'bb']
        builder.root_relation = 'rootrel'
        builder.relations_hierarchy = {
            'a': 'rootrel',
            'bb': 'a'
        }

        entity = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            FIELD.GOBID: 'gobid1',
                            'some': 'value',
                            'bb': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value', FIELD.GOBID: 'gobid2'},
                                    },
                                ]
                            }
                        }
                    }
                ]
            }
        }
        row = {
            '_a': {'some': 'value', FIELD.GOBID: 'gobid1'},
            '_b': {'some_other': 'third value', FIELD.GOBID: 'gobid3'}, # _b is 'truncated' relation name for bb
        }

        expected_result = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            'some': 'value',
                            FIELD.GOBID: 'gobid1',
                            'bb': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value', FIELD.GOBID: 'gobid2'},
                                    },
                                    {
                                        'node': {'some_other': 'third value', FIELD.GOBID: 'gobid3'},
                                    }
                                ]
                            }
                        },
                    }
                ]
            },
        }

        builder._add_row_to_entity(row, entity)
        self.assertEqual(entity, expected_result)

    def test_add_row_to_entity_keyerror_on_relation_from_row(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a']
        entity = {'some': 'entity'}
        row = {}

        with self.assertRaises(KeyError):
            builder._add_row_to_entity(row, entity)

    def test_add_row_to_entity_empty_object(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a', 'b']
        builder.root_relation = 'rootrel'
        builder.relations_hierarchy = {
            'a': 'rootrel',
            'b': 'a'
        }

        entity = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            FIELD.GOBID: 'gobid1',
                            'some': 'value',
                            'b': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value', FIELD.GOBID: 'gobid2'},
                                    },
                                ]
                            }
                        }
                    }
                ]
            }
        }
        row = {
            '_a': {'some': 'value', FIELD.GOBID: 'gobid1'},
            '_b': {'some_other': None, FIELD.GOBID: None},
        }

        expected_result = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            'some': 'value',
                            FIELD.GOBID: 'gobid1',
                            'b': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value', FIELD.GOBID: 'gobid2'},
                                    },
                                ]
                            }
                        },
                    }
                ]
            },
        }

        builder._add_row_to_entity(row, entity)
        self.assertEqual(entity, expected_result)

    def test_add_row_to_entity_double_without_gobid(self):
        builder = self.get_instance()
        builder.evaluation_order = ['a', 'b']
        builder.root_relation = 'rootrel'
        builder.relations_hierarchy = {
            'a': 'rootrel',
            'b': 'a'
        }

        entity = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            FIELD.GOBID: 'gobid1',
                            'some': 'value',
                            'b': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value', FIELD.GOBID: 'gobid2'},
                                    },
                                ]
                            }
                        }
                    }
                ]
            }
        }
        row = {
            '_a': {'some': 'value', FIELD.GOBID: 'gobid1'},
            '_b': {'some_other': 'val', FIELD.GOBID: None},
        }

        expected_result = {
            'existing': 'value',
            'a': {
                'edges': [
                    {
                        'node': {
                            'some': 'value',
                            FIELD.GOBID: 'gobid1',
                            'b': {
                                'edges': [
                                    {
                                        'node': {'some_other': 'value', FIELD.GOBID: 'gobid2'},
                                    },
                                    {
                                        'node': {'some_other': 'val', FIELD.GOBID: None},
                                    },
                                ]
                            }
                        },
                    }
                ]
            },
        }

        # Add twice. Rows should only appear once
        builder._add_row_to_entity(row, entity)
        builder._add_row_to_entity(row, entity)
        self.assertEqual(entity, expected_result)

    def test_build_entity(self):
        builder = self.get_instance()
        collected_rows = [
            {'a': 4, 'b': 5, '_relation': 'somerel'},
            {'a': 4, 'b': 5, '_relation': 'someotherrel'}
        ]

        builder._add_row_to_entity = MagicMock()
        builder._clear_gobids = MagicMock()
        builder._add_sourcevalues_to_row = MagicMock()

        result = builder._build_entity(collected_rows)
        self.assertEqual({
            'node': {
                'a': 4,
                'b': 5
            }
        }, result)
        self.assertEqual(builder._resolver.resolve_row.call_count, 2)  # resolve row and resolve result

        self.assertEqual(2, builder._add_sourcevalues_to_row.call_count)
        builder._add_row_to_entity.assert_has_calls([
            call(collected_rows[0], {'a': 4, 'b': 5}),
            call(collected_rows[1], {'a': 4, 'b': 5}),
        ])
        builder._clear_gobids.assert_called_with(collected_rows)

    def test_build_entity_no_rows(self):
        builder = self.get_instance()

        self.assertIsNone(builder._build_entity([]))

    def test_clear_gobids(self):
        builder = self.get_instance()
        builder.relations_hierarchy = {
            'rela': '',
            'relb': ''
        }

        collected_rows = [
            {
                '_rela': {
                    FIELD.GOBID: 'someval',
                    'a': 'b',
                },
                '_relb': {
                    FIELD.GOBID: 'some other val',
                    'b': 'c',
                },
                'key': 'value',
            }
        ]

        builder._clear_gobids(collected_rows)

        self.assertEqual([{
            '_rela': {
                'a': 'b',
            },
            '_relb': {
                'b': 'c',
            },
            'key': 'value',
        }], collected_rows)

    def test_get_requested_sourcevalues(self):
        builder = self.get_instance()
        builder.selections = {
            'relationA': {
                'fields': [FIELD.SOURCE_VALUE, 'fieldA', 'fieldB', 'fieldC'],
            },
            'relationB': {
                'fields': [],
            },
            'relationC': {
                'fields': [FIELD.SOURCE_INFO, 'fieldD'],
            },
            'relationD': {
                'fields': [FIELD.SOURCE_INFO, FIELD.SOURCE_VALUE],
            },
        }

        self.assertEqual({
            'relationA': [FIELD.SOURCE_VALUE],
            'relationB': [],
            'relationC': [FIELD.SOURCE_INFO],
            'relationD': [FIELD.SOURCE_VALUE, FIELD.SOURCE_INFO],
        }, builder._get_requested_sourcevalues())

    @patch("gobapi.graphql_streaming.response.dict_to_camelcase", lambda x: x)
    @patch("gobapi.graphql_streaming.response.stream_response", lambda x: 'streamed_' + x)
    def test_iter(self):
        builder = self.get_instance()
        builder._determine_relation_evaluation_order = MagicMock(return_value=('eval order', 'root rel'))
        builder.rows = [
            {FIELD.GOBID: '1', 'val': 'a'},
            {FIELD.GOBID: '1', 'val': 'b'},
            {FIELD.GOBID: '2', 'val': 'c'},
            {FIELD.GOBID: '3', 'val': 'd'},
            {FIELD.GOBID: '4', 'val': 'e'},
            {FIELD.GOBID: '4', 'val': 'f'},
        ]

        # Simply adds all the values of the rows currently buffered in collected_rows
        builder._build_entity = lambda x: "".join([i['val'] for i in x])

        result = []

        for row in builder:
            result.append(row)

        # Trailing newline character for successful response is added by decorator
        expected_result = ['streamed_ab\n', 'streamed_c\n', 'streamed_d\n', 'streamed_ef\n', '\n']

        self.assertEqual(expected_result, result)
        self.assertEqual('eval order', builder.evaluation_order)
        self.assertEqual('root rel', builder.root_relation)

    def test_determine_relation_evaluation_order(self):
        builder = self.get_instance(relations_hierarchy={
            'rootrel': None,
            'child': 'rootrel',
            'grandchild': 'child',
            'sibling': 'child',
            'lastinline': 'grandchild'
        })

        result = builder._determine_relation_evaluation_order()

        self.assertEqual(result, (['child', 'grandchild', 'sibling', 'lastinline'], 'rootrel'))

    def test_determine_relation_evaluation_order_invalid(self):
        builder = self.get_instance(relations_hierarchy={
            'rootrel': None,
            'child': 'rootrel',
            'grandchild': 'child',
            'sibling': 'child',
            'lastinline': 'grandchild',
            'dangling': 'nonexistent'
        })

        with self.assertRaises(GOBException):
            builder._determine_relation_evaluation_order()

    def test_public_meta_fields_in_result(self):
        pub_meta_fields = {pub_field: str(num) for num, pub_field in enumerate(PUBLIC_META_FIELDS)}
        builder = self.get_instance()
        builder._determine_relation_evaluation_order = MagicMock(return_value=([], 'root rel'))
        builder.rows = [
            {FIELD.GOBID: '1', 'val': 'a'} | pub_meta_fields,
            {FIELD.GOBID: '2', 'val': 'b'} | pub_meta_fields
        ]

        expected = [
            '{"node": {"val": "a", "version": "0", "dateCreated": "1", "dateConfirmed": "2", "dateModified": "3", '
            '"dateDeleted": "4", "expirationDate": "5"}}\n',
            '{"node": {"val": "b", "version": "0", "dateCreated": "1", "dateConfirmed": "2", "dateModified": "3", '
            '"dateDeleted": "4", "expirationDate": "5"}}\n',
            '\n'
        ]
        self.assertEqual(expected, list(builder))
