import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page."""
    rv = client.get('/')
    assert b'Enter your search term' in rv.data

def test_valid_search_term(client):
    """Test submitting a valid search term."""
    rv = client.post('/', data=dict(search='ValidTerm123'), follow_redirects=True)
    assert b'Search Result' in rv.data
    assert b'ValidTerm123' in rv.data

def test_invalid_search_term(client):
    """Test submitting an invalid search term."""
    rv = client.post('/', data=dict(search='invalid<term>'))
    assert b'Enter your search term' in rv.data
    assert b'Invalid input. Please enter a valid search term.' in rv.data
    assert b'Search Result' not in rv.data
