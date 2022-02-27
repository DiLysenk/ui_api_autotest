import requests
from json.decoder import JSONDecodeError


class Get:

    def __init__(self, url, end_point):
        self.url: str = url
        self.end_point: str = end_point

    def get_request(self):
        try:
            response = requests.get(self.url + self.end_point)
        except ConnectionError:
            raise AssertionError('Ресурс не доступен')
        self._check_status(response)
        return response



    def _parameters_for_json(self, **args):
        return args

    def _headers(self, **args):
        return args

    def _body(self, **args):
        return args
