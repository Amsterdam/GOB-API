import unittest

from graphene import ObjectType, Argument, String, Schema

from gobapi.graphql.scalars import Date, DateTime
from gobapi.middleware import CustomDirectivesMiddleware, CustomDirectiveMeta, BaseCustomDirective


class QueryRoot(ObjectType):
    date_value = Date(value=Argument(Date))
    datestr_value = Date(value=Argument(String))
    datetime_value = DateTime(value=Argument(DateTime))

    @staticmethod
    def resolve_date_value(root, info, value=None):
        return value

    @staticmethod
    def resolve_datestr_value(root, info, value=None):
        return value

    @staticmethod
    def resolve_datetime_value(root, info, value=None):
        return value


schema = Schema(query=QueryRoot, directives=CustomDirectiveMeta.get_all_directives())


class ConcreteDirective(BaseCustomDirective):
    """My concrete example."""


class TestBaseCustomDirective(unittest.TestCase):

    def setUp(self) -> None:
        self.instance = ConcreteDirective()

    def test_get_name(self):
        self.assertEqual(self.instance.get_name(), "concrete")

    def test_get_args(self):
        self.assertEqual(self.instance.get_args(), {})

    def test_description(self):
        self.assertEqual(self.instance.description, "My concrete example.")

    def test_process(self):
        result = self.instance.process("test", None, None, None)
        self.assertEqual(result, "test")


class TestDirectiveMiddleware(unittest.TestCase):

    def test_format_date(self):
        result = self._execute(
            'query($test: Date!) { dateValue(value: $test) @formatdate(format: "%Y-%m") }',
            variable_values={"test": "2020-2-1"}
        )
        self.assertEqual(result.data["dateValue"], "2020-02")

    def test_format_date_str(self):
        result = self._execute(
            'query($test: String!) { datestrValue(value: $test) @formatdate(format: "%Y-%m") }',
            variable_values={"test": "2020-02-01"}
        )
        self.assertEqual(result.data["datestrValue"], "2020-02-01")

    def test_format_datetime(self):
        result = self._execute(
            'query($test: DateTime!) { datetimeValue(value: $test) @formatdate(format: "%Y-%m") }',
            variable_values={"test": "2020-02-01T01:00:00.00"}
        )
        self.assertEqual(result.data["datetimeValue"], "2020-02")

    def test_directive_not_defined(self):
        query = '{ dateValue(value: "2020-1-1") @blah(format: "%Y-%m-%d") }'
        self.assertRaises(AssertionError, self._execute, query)

    def test_no_directive(self):
        result = self._execute('{ dateValue(value: "2020-1-1") }')
        self.assertEqual(result.data["dateValue"], "2020-01-01")

        result = self._execute('{ datetimeValue(value: "2020-02-01T01:00:00.00") }')
        self.assertEqual(result.data["datetimeValue"], "2020-02-01T01:00:00")

    def _execute(self, query, **kwargs):
        result = schema.execute(query, middleware=[CustomDirectivesMiddleware()], **kwargs)
        if result.errors:
            print(result.errors)
        self.assertFalse(bool(result.errors))
        return result
