from unittest import TestCase, mock
from unittest.mock import patch, MagicMock

from gobcore.secure.request import ACCESS_TOKEN_HEADER
from gobapi.auth.routes import secure_route, public_route


class TestAuth(TestCase):

    @patch("gobapi.auth.routes.extract_roles")
    def test_secure_route(self, mock_extract_roles):
        mock_request = MagicMock()

        with patch("gobapi.auth.routes.request", mock_request):

            func = lambda *args, **kwargs: "Any result"

            wrapped_func = secure_route("any rule", func)

            mock_request.headers = {}
            result = wrapped_func()
            self.assertEqual(result, (mock.ANY, 403))

            mock_request.headers = {
                ACCESS_TOKEN_HEADER: "any token"
            }

            result = wrapped_func()
            self.assertEqual(result, "Any result")
            self.assertEqual(mock_extract_roles.return_value, mock_request.roles)

    @patch('gobapi.auth.routes.SECURE_ARGS', ['secure_arg'])
    @patch('gobapi.auth.routes.Authority')
    def test_public_route(self, mock_authority_class):
        mock_request = MagicMock()

        with patch("gobapi.auth.routes.request", mock_request):
            func = lambda *args, **kwargs: "Any result"

            mock_authority = mock.MagicMock()
            mock_authority.allows_access.return_value = True
            mock_authority_class.return_value = mock_authority

            wrapped_func = public_route("any rule", func)

            mock_request.headers = {}
            mock_request.args = {}
            result = wrapped_func()
            self.assertEqual(result, "Any result")

            mock_request.headers = {}
            mock_request.args = {'secure_arg': "any secure_arg"}
            result = wrapped_func()
            self.assertEqual(result, (mock.ANY, 403))

            mock_request.headers = {}
            mock_request.args = {}
            mock_authority.allows_access.return_value = False
            result = wrapped_func()
            self.assertEqual(result, (mock.ANY, 403))

            mock_authority.allows_access.return_value = True

            mock_request.headers = {
                ACCESS_TOKEN_HEADER: "any token",
            }
            result = wrapped_func()
            self.assertEqual(result, (mock.ANY, 400))

    @patch('gobapi.auth.routes._secure_headers_detected')
    def test_secure_headers_detected(self, mock_secure_headers):
        mock_request = MagicMock()

        with patch("gobapi.auth.routes.request", mock_request):

            # Assure that public requests test for secure headers
            func = lambda *args, **kwargs: "Any result"
            wrapped_func = public_route("any rule", func)
            wrapped_func()
            mock_secure_headers.assert_called()

    @patch('gobapi.auth.routes._issue_fraud_warning')
    def test_fraud_warning_issued(self, mock_fraud_warning):
        mock_request = MagicMock()

        with patch("gobapi.auth.routes.request", mock_request):

            # Assure that compromised public requests are signalled
            func = lambda *args, **kwargs: "Any result"
            mock_request.headers = {
                ACCESS_TOKEN_HEADER: "any token"
            }
            wrapped_func = public_route("any rule", func)
            wrapped_func()
            mock_fraud_warning.assert_called()
