import pytest

from flask import session

"""
def test_register(client):
    response_code = client.get('/register').status_code
    assert response_code == 200

    response = client.post(
        '/register',
        data={'username': 'test', 'password': 'Password123'}
    )
    assert response.headers['Location'] == '/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('test', 'password', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
))
def test_register_with_invalid_password(client, username, password, message):
    response = client.post(
        '/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client):


    status_code = client.get('/login').status_code
    assert status_code == 200

    # register the user first
    client.post(
        '/register',
        data={'username': 'test', 'password': 'Password123'}
    )
    response = client.post(
        '/login',
        data={'username': 'test', 'password': 'Password123'})
    assert response.headers['Location'] == "/"

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'test'


def test_logout(client):


    # register the usr first
    client.post(
        '/register',
        data={'username': 'test', 'password': 'Password123'}
    )
    # login
    client.post(
        '/login',
        data={'username': 'test', 'password': 'Password123'})

    with client:
        # check that the user no long exists in the session
        client.get('/logout')
        assert 'user_id' not in session


def test_index(client):
    # check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200

"""