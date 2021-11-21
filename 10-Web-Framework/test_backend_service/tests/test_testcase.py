import requests
import datetime


def test_add():
    r = requests.post(
        'http://127.0.0.1:5000/testcase',
        json={
            'name': f'name {str(datetime.datetime.now())}',
            'description': 'd',
            'data': ''
        }
    )
    assert r.status_code == 200
    assert r.json()['msg'] == 'ok'
