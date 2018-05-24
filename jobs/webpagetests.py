import requests
import os


class WebPageTests(object):
    def __init__(self):
        self.url_run = os.environ["webpagetests_run"]
        self.url_response = os.environ["webpagetests_response"]
        self.api_key = os.environ["webpagetests_api"]
        # http://www.webpagetest.org/getkey.php
    def run_tests(self, request):
        params = dict(
            k=self.api_key,
            label=request['alias'],
            f='json',
            location="{}:{}.{}".format(request['location'], request['browser'], request['speed']),
            url=request['url'],
            noopt=1
        )

        resp = requests.get(url=self.url_run, params=params)
        return resp.json()['data']['testId']

    def test_result(self, id_test):
        params = dict(
            test=id_test
        )
        resp = requests.get(url=self.url_response, params=params)

        return resp.json()
