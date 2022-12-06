from unittest import TestCase
from unittest.mock import Mock

from gobapi.dump.config import JSON_TYPES
from gobapi.dump.csv import _csv_line, _csv_value, _csv_reference_values, _csv_values, CsvDumper


class TestCsvDumper(TestCase):

    def setUp(self) -> None:
        self.model = {
            'catalog': 'any catalog',
            'entity_id': 'any_entity_id',
            'fields': {},
            'all_fields': {
                'any_entity_id': {'type': 'GOB.String'},
                'reference': {'type': 'GOB.Reference'},
                'json': {'type': 'GOB.JSON', 'attributes': {'a': 'GOB.String', 'b': 'GOB.String'}},
                'incdate': {'type': 'GOB.IncompleteDate', 'attributes': {'formatted': {"type": "GOB.String"}}}
            }
        }

        self.mock_entity = Mock()
        self.mock_entity.any_entity_id = 'value_a'
        self.mock_entity.reference = {'bronwaarde': 'value_ref'}
        self.mock_entity.json = {'a': 'some a', 'b': 'some b'}
        self.mock_entity.incdate = {'year': 2021, 'month': 1, 'day': 2}

    def test_init_model_is_none(self):
        dumper = CsvDumper([])
        self.assertEqual(dumper.field_specs, {})
        self.assertEqual(dumper.field_order, [])
        self.assertEqual(dumper.field_names, [])

    def test_get_field_names(self):
        dumper = CsvDumper([], model=self.model)
        expected = [
            'any_entity_id',
            'ref',
            'reference_bronwaarde',
            'json_a',
            'json_b',
            'incdate_formatted'
        ]
        self.assertEqual(dumper.field_names, expected)

    def test_csv_header(self):
        dumper = CsvDumper([], model=self.model)
        expected = '"any_entity_id";"ref";"reference_bronwaarde";"json_a";"json_b";"incdate_formatted"\n'
        self.assertEqual(dumper._csv_header(), expected)

    def test_csv_record(self):
        dumper = CsvDumper([], model=self.model)
        expected = ';;;;;\n'
        self.assertEqual(dumper._csv_record(None), expected)

        expected = '"value_a";"value_a";"value_ref";"some a";"some b";"2021-01-02"\n'
        self.assertEqual(dumper._csv_record(self.mock_entity), expected)

    def test_iterate(self):
        dumper = CsvDumper([], model=self.model)
        value = [item for item in dumper]
        self.assertEqual(value, [])

        header = '"any_entity_id";"ref";"reference_bronwaarde";"json_a";"json_b";"incdate_formatted"\n'
        line1 = '"value_a";"value_a";"value_ref";"some a";"some b";"2021-01-02"\n'

        # header is True
        dumper = CsvDumper([self.mock_entity], model=self.model)
        value = [item for item in dumper]
        self.assertEqual(value, [header, line1])

        # header is False
        dumper = CsvDumper([self.mock_entity], model=self.model, header=False)
        value = [item for item in dumper]
        self.assertEqual(value, [line1])


class TestCSV(TestCase):

    def test_csv_line(self):
        result = _csv_line([])
        self.assertEqual(result, "\n")

        result = _csv_line(["a", "b"])
        self.assertEqual(result, "a;b\n")

    def test_csv_value(self):
        result = _csv_value(None)
        self.assertEqual(result, "")

        result = _csv_value(0)
        self.assertEqual(result, "0")

        result = _csv_value(0.5)
        self.assertEqual(result, "0.5")

        result = _csv_value("s")
        self.assertEqual(result, '"s"')

        result = _csv_value({})
        self.assertEqual(result, '"{}"')

        result = _csv_value("a\r\nb\nc")
        self.assertEqual(result, '"a b c"')

        result = _csv_value("a\"b\"")
        self.assertEqual(result, '"a""b"""')

    def test_csv_reference_values(self):
        spec = {'type': 'GOB.Reference'}
        value = {}
        result = _csv_reference_values(value, spec)
        self.assertEqual(result, [''])

        value = {'id': 'any id', 'bronwaarde': 'any bronwaarde'}
        result = _csv_reference_values(value, spec)
        self.assertEqual(result, ['"any bronwaarde"'])

        # defaults to ManyReference
        spec = {'type': 'any type'}
        values = []
        result = _csv_reference_values(values, spec)
        self.assertEqual(result, ['[]'])

        spec = {'type': 'GOB.ManyReference'}
        values = [value]
        result = _csv_reference_values(values, spec)
        self.assertEqual(result, ['["any bronwaarde"]'])

        spec = {'type': 'GOB.ManyReference'}
        values = [value, value]
        result = _csv_reference_values(values, spec)
        self.assertEqual(result, ['["any bronwaarde","any bronwaarde"]'])

    def test_csv_values(self):
        value = None
        result = _csv_values(None, {'type': 'any type'})
        self.assertEqual(result, [_csv_value(value)])

        value = {}
        spec = {'type': 'GOB.Reference', 'ref': 'any catalog:any collection'}
        result = _csv_values(value, spec)
        self.assertEqual(result, _csv_reference_values(value, spec))

        value = None
        spec = {'type': 'GOB.Reference', 'ref': 'any catalog:any collection'}
        result = _csv_values(value, spec)
        self.assertEqual(result, _csv_reference_values(value, spec))

        for json_type in JSON_TYPES:
            value = {'a': 1, 'b': 'any value', 'c': 'some other value'}
            spec = {'type': json_type, 'attributes': {'a': 'some a', 'b': 'some b'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['1', '"any value"'])

            value = {'a': 1}
            spec = {'type': json_type, 'attributes': {'a': 'some a', 'b': 'some b'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['1', ''])

            # Test JSON many values
            value = [{'a': 1}, {'a': 2}]
            spec = {'type': json_type, 'attributes': {'a': 'some a'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['[1,2]'])

            value = [{'a': '1'}, {'a': '2'}]
            spec = {'type': json_type, 'attributes': {'a': 'some a'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['["1","2"]'])

            value = [{'a': '1'}, {'a': '2'}]
            spec = {'type': json_type, 'attributes': {'a': 'some a', 'b': 'some b'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['["1","2"]', '["",""]'])

            value = [{'a': '1'}, {'a': '2'}]
            spec = {'type': json_type, 'attributes': {'a': 'some a', 'b': 'some b'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['["1","2"]', '["",""]'])

            value = None
            spec = {'type': json_type, 'attributes': {'a': 'some a', 'b': 'some b'}}
            result = _csv_values(value, spec)
            self.assertEqual(result, ['', ''])
