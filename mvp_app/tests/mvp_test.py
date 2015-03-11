# -*- coding: utf-8 -*-
#Tests for MVP app
#https://github.com/mitsuhiko/flask/blob/master/examples/flaskr/test_flaskr.py

import mvp_app
import pytest

@pytest.fixture
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)