from unittest import mock
import os
import json
import unittest

from gobcore.typesystem.gob_types import DateTime, String
from gobcore.typesystem.gob_secure_types import SecureString
from gobcore.secure.crypto import read_protect
from gobapi.json import APIGobTypeJSONEncoder

class TestJsonEncoding(unittest.TestCase):

    @mock.patch('gobapi.json.serialize.secure_value')
    @mock.patch.dict(os.environ,{'SECURE_SALT':'insecure', 'SECURE_PASSWORD':'insecure'})
    def test_json(self, mock_serialize_secure_value):
        gob_type = DateTime.from_value("2019-01-01T10:00:00.123456")
        to_json = json.dumps({'datetime': gob_type}, cls=APIGobTypeJSONEncoder)
        self.assertEqual('{"datetime": "2019-01-01T10:00:00.123456"}', to_json)

        gob_type = DateTime.from_value("2019-01-01T10:00:00.000000")
        to_json = json.dumps({'datetime': gob_type}, cls=APIGobTypeJSONEncoder)
        self.assertEqual('{"datetime": "2019-01-01T10:00:00"}', to_json)

        # Test is other types use the regular JSONEncoder
        gob_type = String.from_value(123)
        to_json = json.dumps({'string': gob_type}, cls=APIGobTypeJSONEncoder)
        self.assertEqual('{"string": "123"}', to_json)

        mock_serialize_secure_value.return_value = "secure value"
        gob_type = SecureString.from_value(read_protect("any string"), level=5)
        to_json = json.dumps({'string': gob_type}, cls=APIGobTypeJSONEncoder)
        self.assertEqual('{"string": "secure value"}', to_json)
