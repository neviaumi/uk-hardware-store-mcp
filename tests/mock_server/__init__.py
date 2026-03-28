import os

import pytest
import pytest_httpserver.httpserver as httpserver

import app.config as config


def mock_response_data(fileName: str):
    path = os.path.join(os.path.dirname(__file__), fileName)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def mock_server(httpserver: httpserver.HTTPServer, monkeypatch):
    monkeypatch.setattr(
        config,
        "HOMEBASE_URL",
        httpserver.url_for("/homebase/en-uk"),
    )
    monkeypatch.setattr(
        config,
        "DIY_DOT_COM_URL",
        httpserver.url_for("/b&q"),
    )
    monkeypatch.setattr(
        config,
        "WICKES_URL",
        httpserver.url_for("/wickes"),
    )
    monkeypatch.setattr(
        config,
        "SCREWFIX_URL",
        httpserver.url_for("/screwfix"),
    )
    return httpserver
