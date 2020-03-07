import tempfile

import pytest

import vlabs


@pytest.fixture
def client():
    db_fd, vlabs.app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with vlabs.app.test_client() as client:
        with vlabs.app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(vlabs.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Welcome to Virtual Labs' in rv.response.data