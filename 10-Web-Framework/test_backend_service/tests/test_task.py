import sys
from time import sleep

import requests

sys.path.append("..")
from core.backend import jenkins
from tests.base_testcase import BaseTestCase


class TestTask(BaseTestCase):
    def test_task_post(self):

        pre = jenkins['testcase'].get_last_build().get_number()
        r = requests.post(
            'http://127.0.0.1:5000/task',
            json={'testcases': 'sub_dir'},
            headers={'Authorization': f'Bearer {self.token}'}

        )
        assert r.status_code == 200
        for i in range(10):
            if not jenkins['testcase'].is_queued_or_running():
                break
            else:
                print('wait')
                sleep(1)
        last = jenkins['testcase'].get_last_build().get_number()
        print(pre)
        print(last)
        assert last == pre + 1
