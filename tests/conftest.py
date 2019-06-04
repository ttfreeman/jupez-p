import pytest
import jupez
import config


@pytest.fixture
def app():
    app = jupez.create_app(config, testing=True)
    yield app


@pytest.fixture
def model(monkeypatch, app):
    from ..import mongodb
    model = mongodb

    delete_all_jupes(model)
    yield model
    delete_all_jupes(model)


def delete_all_jupes(model):
    while True:
        jupes, _ = model.list(limit=50)
        if not jupes:
            break
        for jupe in jupes:
            model.delete(jupe['id'])