import json


def test_create_app(client):
    payload = {
        'title': 'My first app',
        'content': 'Test if I can create a new app.'
    }
    resp = client.post(
        '/api/myapp/test_app_name',
        json.dumps(payload),
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.json()['app'] == {
        'name': 'test_app_name',
        'title': 'My first app',
        'content': 'Test if I can create a new app.'
    }
