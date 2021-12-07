# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
import pytest

from app.app import create_app
from app.ext.settings import settings

app = create_app()

client = TestClient(app)


@pytest.fixture()
def api_token():
    # Get Token

    response = client.post(
        headers={"Accept": "application/x-www-form-urlencoded"},
        data={
            "username": settings.API_USERNAME,
            "password": settings.API_PASSWORD,
        },
    )

    result = response.json()
    access_token = result['token']
    token_type = res_json["token_type"]
    return f"{token_type} {access_token}"


def test_get_users():
    response = client.get("/v1/user")
    assert response.status_code == 200


def test_get_clients():
    response = client.get("/v1/clients")
    assert response.status_code == 200
