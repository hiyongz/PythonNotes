import requests


def test_testcase_post():
    r = requests.post(
        'http://127.0.0.1:5000/testcase',
        json={
            'name': "testcase 2",
            "steps": ["step 1", "step 2"]
        }
    )
    assert r.status_code == 200

    r = requests.post(
        'http://127.0.0.1:5000/testcase',
        json={
            'name': "testcase 3",
            "steps": ["step 1", "step 2"]
        }
    )
    assert r.status_code == 200

    r = requests.delete(
        'http://127.0.0.1:5000/testcase',
        json={
            'name': "testcase 3"
        }
    )
    assert r.status_code == 200


def test_suite_testcase_id():
    r = requests.post(
        'http://127.0.0.1:5000/suite',
        json={
            'name': 'suite 1',
            'testcases': [1, 2, 3]
        }
    )
    assert r.status_code == 200


def test_suite_testcase_filename():
    r = requests.post(
        'http://127.0.0.1:5000/suite',
        json={
            'name': 'suite 3',
            'testcases': 'test_python/tests/test_hero.py'
        }
    )
    assert r.status_code == 200

def test_execution():
    r = requests.post(
        'http://127.0.0.1:5000/execution',
        json={
            'suite_id': 3
        }
    )
    assert r.status_code == 200
