import pytest
import json
from app.main import app
from app.models import url_store
from app.utils import is_valid_url, generate_short_code, normalize_url

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear the URL store before each test
        url_store._mappings.clear()
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'URL Shortener API is running'

def test_shorten_url_success(client):
    """Test successful URL shortening."""
    response = client.post('/api/shorten',
                          json={'url': 'https://www.example.com/very/long/url'},
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6
    assert data['short_code'].isalnum()
    assert data['short_url'].endswith(data['short_code'])

def test_shorten_url_missing_url(client):
    """Test shortening with missing URL field."""
    response = client.post('/api/shorten',
                          json={},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Missing' in data['error']

def test_shorten_url_empty_url(client):
    """Test shortening with empty URL."""
    response = client.post('/api/shorten',
                          json={'url': ''},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'empty' in data['error']

def test_shorten_url_invalid_url(client):
    """Test shortening with invalid URL."""
    response = client.post('/api/shorten',
                          json={'url': 'not-a-url'},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid' in data['error']

def test_shorten_url_without_scheme(client):
    """Test shortening URL without scheme (should add https://)."""
    response = client.post('/api/shorten',
                          json={'url': 'www.example.com'},
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

def test_redirect_success(client):
    """Test successful redirect."""
    # First create a short URL
    shorten_response = client.post('/api/shorten',
                                  json={'url': 'https://www.example.com'},
                                  content_type='application/json')
    short_code = shorten_response.get_json()['short_code']
    
    # Test redirect
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'

def test_redirect_nonexistent_code(client):
    """Test redirect with non-existent short code."""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_redirect_invalid_format(client):
    """Test redirect with invalid short code format."""
    response = client.get('/invalid')
    assert response.status_code == 404

def test_stats_success(client):
    """Test getting stats for a valid short code."""
    # First create a short URL
    shorten_response = client.post('/api/shorten',
                                  json={'url': 'https://www.example.com'},
                                  content_type='application/json')
    short_code = shorten_response.get_json()['short_code']
    
    # Access the URL to increment clicks
    client.get(f'/{short_code}', follow_redirects=False)
    client.get(f'/{short_code}', follow_redirects=False)
    
    # Get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['url'] == 'https://www.example.com'
    assert data['short_code'] == short_code
    assert data['clicks'] == 2
    assert 'created_at' in data

def test_stats_nonexistent_code(client):
    """Test getting stats for non-existent short code."""
    response = client.get('/api/stats/abc123')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'not found' in data['error']

def test_stats_invalid_format(client):
    """Test getting stats with invalid short code format."""
    response = client.get('/api/stats/invalid')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid' in data['error']

def test_multiple_requests(client):
    """Test handling of multiple sequential requests."""
    results = []
    
    # Make multiple requests sequentially
    for _ in range(5):
        response = client.post('/api/shorten',
                              json={'url': 'https://www.example.com'},
                              content_type='application/json')
        results.append(response.get_json())
    
    # All requests should succeed
    assert len(results) == 5
    for result in results:
        assert 'short_code' in result
        assert 'short_url' in result
        assert len(result['short_code']) == 6
        assert result['short_code'].isalnum()

def test_utils_is_valid_url():
    """Test URL validation utility function."""
    assert is_valid_url('https://www.example.com') == True
    assert is_valid_url('http://example.com') == True
    assert is_valid_url('https://example.com/path?param=value') == True
    assert is_valid_url('not-a-url') == False
    assert is_valid_url('') == False

def test_utils_generate_short_code():
    """Test short code generation utility function."""
    code = generate_short_code()
    assert len(code) == 6
    assert code.isalnum()
    
    # Test custom length
    code = generate_short_code(8)
    assert len(code) == 8
    assert code.isalnum()

def test_utils_normalize_url():
    """Test URL normalization utility function."""
    assert normalize_url('https://example.com') == 'https://example.com'
    assert normalize_url('http://example.com') == 'http://example.com'
    assert normalize_url('example.com') == 'https://example.com'
    assert normalize_url('www.example.com') == 'https://www.example.com'

def test_thread_safety():
    """Test that the URL store is thread-safe."""
    import threading
    
    # Clear the store
    url_store._mappings.clear()
    
    def add_mapping():
        short_code = generate_short_code()
        url_store.add_mapping(short_code, 'https://example.com')
    
    # Create multiple threads
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=add_mapping)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Should have 10 mappings
    assert len(url_store._mappings) == 10