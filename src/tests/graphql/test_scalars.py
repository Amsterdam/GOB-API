import datetime

import geoalchemy2

from graphql.language import ast
from gobapi.graphql import scalars, BigInt
from gobapi.graphql.scalars import Date, DateTime, GeoJSON


class Session:
    def __init__(self):
        pass

    def scalar(self, geom):
        return geom


class MockManagedSession:

    def __enter__(self):
        self._session = Session()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Geometry:
    def __init__(self, geojson):
        self.geojson = geojson

    def ST_AsGeoJSON(self):
        return self.geojson


def test_date(monkeypatch):
    serialized = Date.serialize(datetime.date(2000, 1, 20))
    assert(serialized == "2000-01-20")

    serialized = Date.serialize("2000-01-20")
    assert(serialized == "2000-01-20")

    class Literal(ast.StringValue):
        def __init__(self, value):
            self.value = value

    parsed_literal = Date.parse_literal(Literal("2000-01-20"))
    assert(parsed_literal == datetime.date(2000, 1, 20))

    parsed_literal = Date.parse_literal(Literal("0020-01-20"))
    assert(parsed_literal == datetime.date(20, 1, 20))

    parsed_literal = Date.parse_literal(Literal("null"))
    assert(parsed_literal == "null")

    parsed_literal = Date.parse_literal("non literal")
    assert(parsed_literal == None)  # value is not parsed


def test_datetime(monkeypatch):
    serialized = DateTime.serialize(datetime.datetime(2000, 1, 20, 12, 0, 0))
    assert(serialized == "2000-01-20T12:00:00")

    serialized = DateTime.serialize("2000-01-20T12:00:00")
    assert(serialized == "2000-01-20T12:00:00")

    # Test patched date for years < 1000
    serialized = DateTime.serialize(datetime.datetime(20, 1, 20, 12, 0, 0))
    assert(serialized == "0020-01-20T12:00:00")

    # Test date with microseconds
    serialized = DateTime.serialize(datetime.datetime(20, 1, 20, 12, 0, 0, 123456))
    assert(serialized == "0020-01-20T12:00:00.123456")

    class Literal(ast.StringValue):
        def __init__(self, value):
            self.value = value
    parsed_literal = DateTime.parse_literal(Literal("2000-01-20T12:00:00.000000"))
    assert(parsed_literal == datetime.datetime(2000, 1, 20, 12, 0, 0))

    parsed_literal = DateTime.parse_literal(Literal("0020-01-20T12:00:00.000000"))
    assert(parsed_literal == datetime.datetime(20, 1, 20, 12, 0, 0))

    parsed_literal = DateTime.parse_literal(Literal("2000-01-20T12:00:00.123456"))
    assert(parsed_literal == datetime.datetime(2000, 1, 20, 12, 0, 0, 123456))

    parsed_literal = DateTime.parse_literal(Literal("null"))
    assert(parsed_literal == "null")

    parsed_literal = DateTime.parse_literal("non literal")
    assert(parsed_literal == None)  # value is not parsed


def test_geojson(monkeypatch):
    monkeypatch.setattr(scalars , "get_session", Session)

    geojson = '{"type": "Point", "coordinates": [100, 100]}'
    geom = Geometry(geojson)

    serialized = GeoJSON.serialize(geom)
    assert(serialized == {"type": "Point", "coordinates": [100, 100]})

    class Literal(ast.StringValue):
        def __init__(self, value):
            self.value = value

    parsed_literal = GeoJSON.parse_literal(Literal('{"type": "Point", "coordinates": [100, 100]}'))
    assert type(parsed_literal) == geoalchemy2.functions.ST_GeomFromText

    parsed_literal = GeoJSON.parse_literal(Literal("null"))
    assert parsed_literal == "null"

    parsed_literal = GeoJSON.parse_literal("non literal")
    assert parsed_literal == None  # value is not parsed


def test_bigint():
    big_num_int = 17_000_000_000
    tests = [
        (big_num_int, big_num_int),
        ('17000000000', big_num_int),
        (17_000_000_000.02, big_num_int),
        (-17_000_000_000, big_num_int*-1),
        (10, 10)
    ]

    class Literal(ast.IntValue):
        def __init__(self, value):
            self.value = value

    for num, expected in tests:
        assert BigInt.parse_literal(Literal(num)) == expected
        assert BigInt.serialize(num) == expected
        assert BigInt.parse_value(num) == expected

    try:
        BigInt.parse_literal(Literal('abcd'))
    except ValueError:
        assert True
    else:
        assert False

    assert BigInt.serialize('abcd') is None
