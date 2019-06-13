import re
import os
import pytest
import config
import jupez


@pytest.fixture
def client():
    db_fd, jupez.app.config['DATABASE'] = tempfile.mkstemp()
    jupez.app.config['TESTING'] = True
    client = jupez.app.test_client()

    with jupez.app.app_context():
        jupez.init_db()

    yield client

    os.close(db_fd)
    os.unlink(jupez.app.config['DATABASE'])


@pytest.fixture
def app():
    app = jupez.create_app(
        config,
        testing=True)
    yield app


@pytest.fixture
def model():
    model=jupez.get_model()
    yield model



def test_list(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data


