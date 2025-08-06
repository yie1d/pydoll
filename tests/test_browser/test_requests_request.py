"""
Tests for pydoll.browser.requests.request module.
"""

import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, Mock, patch
from urllib.parse import urlencode

from pydoll.browser.requests.request import Request
from pydoll.browser.requests.response import HTTPError, Response
from pydoll.protocol.fetch.types import HeaderEntry
from pydoll.protocol.network.events import NetworkEvent
from pydoll.protocol.network.types import CookieParam


@pytest_asyncio.fixture
async def mock_tab():
    """Create a mock Tab instance for testing."""
    tab = Mock()
    tab.network_events_enabled = False
    tab.enable_network_events = AsyncMock()
    tab.disable_network_events = AsyncMock()
    tab.clear_callbacks = AsyncMock()
    tab.on = AsyncMock()
    tab._execute_command = AsyncMock()
    return tab


@pytest_asyncio.fixture
async def request_instance(mock_tab):
    """Create a Request instance for testing."""
    return Request(mock_tab)


class TestRequestInitialization:
    """Test Request class initialization."""

    def test_request_initialization(self, mock_tab):
        """Test Request initialization with tab."""
        request = Request(mock_tab)
        
        assert request.tab == mock_tab
        assert request._network_events_enabled is False
        assert request._requests_sent == []
        assert request._requests_received == []

    def test_request_initialization_preserves_tab_reference(self, mock_tab):
        """Test that Request maintains reference to provided tab."""
        request = Request(mock_tab)
        assert request.tab is mock_tab


class TestRequestMethods:
    """Test HTTP method convenience functions."""

    @pytest.mark.asyncio
    async def test_get_method(self, request_instance):
        """Test GET request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.get('https://example.com', params={'q': 'test'})
            
            mock_request.assert_called_once_with(
                'GET', 'https://example.com', params={'q': 'test'}
            )

    @pytest.mark.asyncio
    async def test_post_method(self, request_instance):
        """Test POST request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.post(
                'https://example.com', 
                data={'key': 'value'}, 
                json={'json_key': 'json_value'}
            )
            
            mock_request.assert_called_once_with(
                'POST', 
                'https://example.com', 
                data={'key': 'value'}, 
                json={'json_key': 'json_value'}
            )

    @pytest.mark.asyncio
    async def test_put_method(self, request_instance):
        """Test PUT request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.put('https://example.com', json={'update': 'data'})
            
            mock_request.assert_called_once_with(
                'PUT', 'https://example.com', data=None, json={'update': 'data'}
            )

    @pytest.mark.asyncio
    async def test_patch_method(self, request_instance):
        """Test PATCH request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.patch('https://example.com', data='patch_data')
            
            mock_request.assert_called_once_with(
                'PATCH', 'https://example.com', data='patch_data', json=None
            )

    @pytest.mark.asyncio
    async def test_delete_method(self, request_instance):
        """Test DELETE request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.delete('https://example.com')
            
            mock_request.assert_called_once_with('DELETE', 'https://example.com')

    @pytest.mark.asyncio
    async def test_head_method(self, request_instance):
        """Test HEAD request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.head('https://example.com')
            
            mock_request.assert_called_once_with('HEAD', 'https://example.com')

    @pytest.mark.asyncio
    async def test_options_method(self, request_instance):
        """Test OPTIONS request method."""
        with patch.object(request_instance, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Mock()
            
            await request_instance.options('https://example.com')
            
            mock_request.assert_called_once_with('OPTIONS', 'https://example.com')


class TestRequestMainMethod:
    """Test main request method functionality."""

    @pytest.mark.asyncio
    async def test_request_success_flow(self, request_instance, mock_tab):
        """Test successful request execution flow."""
        # Mock execute_command response
        mock_result = {
            'result': {
                'result': {
                    'value': {
                        'status': 200,
                        'content': [72, 101, 108, 108, 111],  # "Hello" as bytes
                        'text': 'Hello',
                        'json': {'message': 'success'},
                        'url': 'https://example.com'
                    }
                }
            }
        }
        mock_tab._execute_command.return_value = mock_result
        
        # Mock helper methods
        with patch.object(request_instance, '_extract_received_headers') as mock_extract_headers, \
             patch.object(request_instance, '_extract_sent_headers') as mock_extract_sent, \
             patch.object(request_instance, '_extract_set_cookies') as mock_extract_cookies:
            
            mock_extract_headers.return_value = [HeaderEntry(name='Content-Type', value='application/json')]
            mock_extract_sent.return_value = [HeaderEntry(name='User-Agent', value='Test-Agent')]
            mock_extract_cookies.return_value = [CookieParam(name='session', value='abc123')]
            
            response = await request_instance.request('GET', 'https://example.com')
            
            assert isinstance(response, Response)
            assert response.status_code == 200
            assert response.text == 'Hello'
            assert response.json() == {'message': 'success'}
            assert response.url == 'https://example.com'

    @pytest.mark.asyncio
    async def test_request_with_params(self, request_instance):
        """Test request with query parameters."""
        with patch.object(request_instance, '_build_url_with_params') as mock_build_url, \
             patch.object(request_instance, '_execute_fetch_request') as mock_execute, \
             patch.object(request_instance, '_extract_received_headers') as mock_headers, \
             patch.object(request_instance, '_extract_sent_headers') as mock_sent, \
             patch.object(request_instance, '_extract_set_cookies') as mock_cookies, \
             patch.object(request_instance, '_build_response') as mock_build_response, \
             patch.object(request_instance, '_clear_callbacks') as mock_clear:
            
            mock_build_url.return_value = 'https://example.com?q=test'
            mock_execute.return_value = {'result': {'result': {'value': {}}}}
            mock_headers.return_value = []
            mock_sent.return_value = []
            mock_cookies.return_value = []
            mock_build_response.return_value = Mock()
            
            await request_instance.request('GET', 'https://example.com', params={'q': 'test'})
            
            mock_build_url.assert_called_once_with('https://example.com', {'q': 'test'})

    @pytest.mark.asyncio
    async def test_request_with_json_data(self, request_instance):
        """Test request with JSON data."""
        with patch.object(request_instance, '_build_request_options') as mock_build_options, \
             patch.object(request_instance, '_execute_fetch_request') as mock_execute, \
             patch.object(request_instance, '_extract_received_headers') as mock_headers, \
             patch.object(request_instance, '_extract_sent_headers') as mock_sent, \
             patch.object(request_instance, '_extract_set_cookies') as mock_cookies, \
             patch.object(request_instance, '_build_response') as mock_build_response, \
             patch.object(request_instance, '_clear_callbacks') as mock_clear:
            
            mock_execute.return_value = {'result': {'result': {'value': {}}}}
            mock_headers.return_value = []
            mock_sent.return_value = []
            mock_cookies.return_value = []
            mock_build_response.return_value = Mock()
            
            json_data = {'key': 'value'}
            await request_instance.request('POST', 'https://example.com', json=json_data)
            
            mock_build_options.assert_called_once_with(
                'POST', None, json_data, None
            )

    @pytest.mark.asyncio
    async def test_request_failure_raises_http_error(self, request_instance, mock_tab):
        """Test that request failures raise HTTPError."""
        mock_tab._execute_command.side_effect = Exception("Network error")
        
        with pytest.raises(HTTPError, match="Request failed: Network error"):
            await request_instance.request('GET', 'https://example.com')

    @pytest.mark.asyncio
    async def test_request_always_clears_callbacks(self, request_instance, mock_tab):
        """Test that callbacks are always cleared, even on error."""
        mock_tab._execute_command.side_effect = Exception("Network error")
        
        with patch.object(request_instance, '_clear_callbacks') as mock_clear:
            with pytest.raises(HTTPError):
                await request_instance.request('GET', 'https://example.com')
            
            mock_clear.assert_called_once()


class TestRequestHelperMethods:
    """Test Request helper methods."""

    def test_build_url_with_params_no_params(self, request_instance):
        """Test URL building without parameters."""
        url = 'https://example.com'
        result = request_instance._build_url_with_params(url, None)
        assert result == url

    def test_build_url_with_params_simple(self, request_instance):
        """Test URL building with simple parameters."""
        url = 'https://example.com'
        params = {'q': 'test', 'page': '1'}
        result = request_instance._build_url_with_params(url, params)
        
        assert 'https://example.com?' in result
        assert 'q=test' in result
        assert 'page=1' in result

    def test_build_url_with_params_existing_query(self, request_instance):
        """Test URL building with existing query string."""
        url = 'https://example.com?existing=param'
        params = {'new': 'value'}
        result = request_instance._build_url_with_params(url, params)
        
        assert 'existing=param' in result
        assert 'new=value' in result

    def test_build_request_options_basic(self, request_instance):
        """Test basic request options building."""
        options = request_instance._build_request_options(
            'GET', None, None, None
        )
        
        assert options['method'] == 'GET'
        assert options['headers'] == {}

    def test_build_request_options_with_headers(self, request_instance):
        """Test request options building with headers."""
        headers = [HeaderEntry(name='Authorization', value='Bearer token')]
        
        with patch.object(request_instance, '_convert_header_entries_to_dict') as mock_convert:
            mock_convert.return_value = {'Authorization': 'Bearer token'}
            
            options = request_instance._build_request_options(
                'POST', headers, None, None
            )
            
            assert options['headers'] == {'Authorization': 'Bearer token'}
            mock_convert.assert_called_once_with(headers)

    def test_handle_json_options(self, request_instance):
        """Test JSON data handling."""
        options = {'headers': {}}
        json_data = {'key': 'value'}
        
        request_instance._handle_json_options(options, json_data)
        
        assert options['body'] == json.dumps(json_data)
        assert options['headers']['Content-Type'] == 'application/json'

    def test_handle_data_options_form_data(self, request_instance):
        """Test form data handling."""
        options = {'headers': {}}
        data = {'key': 'value', 'key2': 'value2'}
        
        request_instance._handle_data_options(options, data)
        
        assert options['body'] == urlencode(data, doseq=True)
        assert options['headers']['Content-Type'] == 'application/x-www-form-urlencoded'

    def test_handle_data_options_raw_data(self, request_instance):
        """Test raw data handling."""
        options = {'headers': {}}
        data = 'raw string data'
        
        request_instance._handle_data_options(options, data)
        
        assert options['body'] == data
        assert 'Content-Type' not in options['headers']

    def test_convert_header_entries_to_dict(self, request_instance):
        """Test header entries conversion to dictionary."""
        headers = [
            HeaderEntry(name='Content-Type', value='application/json'),
            HeaderEntry(name='Authorization', value='Bearer token')
        ]
        
        result = request_instance._convert_header_entries_to_dict(headers)
        
        expected = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token'
        }
        assert result == expected

    def test_convert_dict_to_header_entries(self, request_instance):
        """Test dictionary conversion to header entries."""
        headers_dict = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token'
        }
        
        result = request_instance._convert_dict_to_header_entries(headers_dict)
        
        assert len(result) == 2
        # Check that each result is a dictionary with the expected keys
        for header in result:
            assert 'name' in header
            assert 'value' in header
        assert {header['name']: header['value'] for header in result} == headers_dict


class TestRequestCallbackManagement:
    """Test callback registration and management."""

    @pytest.mark.asyncio
    async def test_register_callbacks_enables_network_events(self, request_instance, mock_tab):
        """Test that registering callbacks enables network events."""
        mock_tab.network_events_enabled = False
        
        await request_instance._register_callbacks()
        
        mock_tab.enable_network_events.assert_called_once()
        assert request_instance._network_events_enabled is True

    @pytest.mark.asyncio
    async def test_register_callbacks_skips_if_already_enabled(self, request_instance, mock_tab):
        """Test that network events are not re-enabled if already active."""
        mock_tab.network_events_enabled = True
        
        await request_instance._register_callbacks()
        
        mock_tab.enable_network_events.assert_not_called()
        assert request_instance._network_events_enabled is False

    @pytest.mark.asyncio
    async def test_register_callbacks_subscribes_to_events(self, request_instance, mock_tab):
        """Test that all required network events are subscribed to."""
        await request_instance._register_callbacks()
        
        expected_events = [
            NetworkEvent.REQUEST_WILL_BE_SENT,
            NetworkEvent.REQUEST_WILL_BE_SENT_EXTRA_INFO,
            NetworkEvent.RESPONSE_RECEIVED,
            NetworkEvent.RESPONSE_RECEIVED_EXTRA_INFO
        ]
        
        assert mock_tab.on.call_count == len(expected_events)
        called_events = [call[0][0] for call in mock_tab.on.call_args_list]
        
        for event in expected_events:
            assert event in called_events

    @pytest.mark.asyncio
    async def test_clear_callbacks_disables_network_events(self, request_instance, mock_tab):
        """Test that clearing callbacks disables network events if they were enabled."""
        request_instance._network_events_enabled = True
        
        await request_instance._clear_callbacks()
        
        mock_tab.disable_network_events.assert_called_once()
        mock_tab.clear_callbacks.assert_called_once()
        assert request_instance._network_events_enabled is False

    @pytest.mark.asyncio
    async def test_clear_callbacks_skips_disable_if_not_enabled(self, request_instance, mock_tab):
        """Test that network events are not disabled if not enabled by request."""
        request_instance._network_events_enabled = False
        
        await request_instance._clear_callbacks()
        
        mock_tab.disable_network_events.assert_not_called()
        mock_tab.clear_callbacks.assert_called_once()


class TestRequestCookieExtraction:
    """Test cookie extraction functionality."""

    def test_parse_cookie_line_valid(self, request_instance):
        """Test parsing valid cookie line."""
        line = 'session_id=abc123; Path=/; HttpOnly'
        
        result = request_instance._parse_cookie_line(line)
        
        assert result is not None
        assert result['name'] == 'session_id'
        assert result['value'] == 'abc123'

    def test_parse_cookie_line_invalid(self, request_instance):
        """Test parsing invalid cookie line."""
        line = 'invalid_cookie_without_equals'
        
        result = request_instance._parse_cookie_line(line)
        
        assert result is None

    def test_parse_cookie_line_with_complex_value(self, request_instance):
        """Test parsing cookie with complex value."""
        line = 'complex=value=with=equals; Secure'
        
        result = request_instance._parse_cookie_line(line)
        
        assert result is not None
        assert result['name'] == 'complex'
        assert result['value'] == 'value=with=equals'

    def test_add_unique_cookies_no_duplicates(self, request_instance):
        """Test adding unique cookies without duplicates."""
        existing_cookies = [CookieParam(name='existing', value='value1')]
        new_cookies = [
            CookieParam(name='new', value='value2'),
            CookieParam(name='existing', value='value1')  # Duplicate
        ]
        
        request_instance._add_unique_cookies(existing_cookies, new_cookies)
        
        assert len(existing_cookies) == 2
        cookie_names = [cookie['name'] for cookie in existing_cookies]
        assert 'existing' in cookie_names
        assert 'new' in cookie_names

    def test_parse_set_cookie_header_multiline(self, request_instance):
        """Test parsing multi-line Set-Cookie header."""
        header = 'cookie1=value1; Path=/\ncookie2=value2; Secure'
        
        result = request_instance._parse_set_cookie_header(header)
        
        assert len(result) == 2
        assert result[0]['name'] == 'cookie1'
        assert result[1]['name'] == 'cookie2'


class TestRequestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_request_with_empty_url(self, request_instance):
        """Test request with empty URL."""
        with patch.object(request_instance, '_execute_fetch_request') as mock_execute, \
             patch.object(request_instance, '_extract_received_headers') as mock_headers, \
             patch.object(request_instance, '_extract_sent_headers') as mock_sent, \
             patch.object(request_instance, '_extract_set_cookies') as mock_cookies, \
             patch.object(request_instance, '_build_response') as mock_build_response, \
             patch.object(request_instance, '_clear_callbacks') as mock_clear:
            
            mock_execute.return_value = {'result': {'result': {'value': {}}}}
            mock_headers.return_value = []
            mock_sent.return_value = []
            mock_cookies.return_value = []
            mock_build_response.return_value = Mock()
            
            await request_instance.request('GET', '')
            
            mock_execute.assert_called_once()

    def test_build_url_with_special_characters(self, request_instance):
        """Test URL building with special characters in parameters."""
        url = 'https://example.com'
        params = {'q': 'hello world', 'special': 'value&with=chars'}
        
        result = request_instance._build_url_with_params(url, params)
        
        assert 'hello+world' in result or 'hello%20world' in result
        assert 'value%26with%3Dchars' in result

    def test_handle_data_options_with_bytes(self, request_instance):
        """Test handling raw bytes data."""
        options = {'headers': {}}
        data = b'binary data'
        
        request_instance._handle_data_options(options, data)
        
        assert options['body'] == data
        assert 'Content-Type' not in options['headers']

    def test_convert_header_entries_empty_list(self, request_instance):
        """Test converting empty header entries list."""
        result = request_instance._convert_header_entries_to_dict([])
        assert result == {}

    def test_convert_dict_to_header_entries_empty_dict(self, request_instance):
        """Test converting empty dictionary to header entries."""
        result = request_instance._convert_dict_to_header_entries({})
        assert result == []