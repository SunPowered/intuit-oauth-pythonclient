
 # Copyright (c) 2018 Intuit
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #  http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.

"""Test module for intuitlib.client
"""
import pytest
import mock

try:
    from urllib.parse import urlparse, parse_qs, urlsplit
except ImportError:
    from urlparse import urlparse, parse_qs, urlsplit

from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
from tests.helper import MockResponse

@pytest.fixture()
def auth_client_default():
    return AuthClient('clientId','secret','https://www.mydemoapp.com/oauth-redirect','sandbox')

@pytest.fixture()
def auth_client(auth_client_default):
    auth_client_default._discovery_doc = {
        'authorization_endpoint': 'http://test',
        'token_endpoint': 'http://test',
        'revocation_endpoint': 'http://test',
        'issuer': 'http://test',
        'jwks_uri': 'http://test',
        'userinfo_endpoint': 'http://test',
    }
    return auth_client_default

class TestClient():
    
    def mock_request(self, status=200, content=None):
        return MockResponse(status=status, content=content)

    def test_input_all(self, auth_client):
        
        auth_client.access_token = None
        
        with pytest.raises(ValueError):
            auth_client.refresh()
        
        with pytest.raises(ValueError):
            auth_client.revoke()
        
        with pytest.raises(ValueError):
            auth_client.get_user_info()

    def test_get_authorization_url_without_csrf(self, auth_client):
        uri = auth_client.get_authorization_url([Scopes.ACCOUNTING])
        params = parse_qs(urlsplit(uri).query)
        param_values_to_string = {k: v[0] for k, v in params.items()}

        auth_params = {
            'client_id': 'clientId',
            'response_type': 'code',
            'scope': 'com.intuit.quickbooks.accounting',
            'redirect_uri': 'https://www.mydemoapp.com/oauth-redirect',
            'state': auth_client.state_token
        }
        assert auth_params == param_values_to_string

    @mock.patch('intuitlib.utils.requests.Session.request')
    def test_exceptions_all_bad_request(self, mock_post, auth_client):
        mock_resp = self.mock_request(status=400)
        mock_post.return_value = mock_resp
        
        # auth_client = auth_client_default
        with pytest.raises(AuthClientError):
            auth_client.get_bearer_token('test_code', realm_id='realm')
        
        with pytest.raises(AuthClientError):
            auth_client.refresh(refresh_token='test_token')

        with pytest.raises(AuthClientError):
            auth_client.revoke(token='test_token')

        with pytest.raises(AuthClientError):
            auth_client.get_user_info(access_token='token')
    
    @mock.patch('intuitlib.utils.requests.Session.request')
    def test_get_user_info_ok(self, mock_session, auth_client):
        mock_resp = self.mock_request(status=200, content={
            'givenName': 'Test'
        })
        mock_session.return_value = mock_resp
        
        response = auth_client.get_user_info(access_token='token')
        assert response.json()['givenName'] == 'Test'

    @mock.patch('intuitlib.utils.requests.Session.request')
    def test_revoke_ok(self, mock_session, auth_client):
        mock_resp = self.mock_request(status=200)
        mock_session.return_value = mock_resp
        
        response = auth_client.revoke(token='token')
        assert response

if __name__ == '__main__':
    pytest.main()