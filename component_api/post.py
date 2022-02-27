import requests


class Post:

    def __init__(self, url, end_point):
        self.url: str = url
        self.end_point: str = end_point

    def get_request(self):
        try:
            response = requests.post(self.url + self.end_point)
        except ConnectionError:
            raise AssertionError('Ресурс не доступен')
        self._check_status(response)
        return response

    def _check_status(self, response):
        if response.status_code == 500:
            raise AssertionError(f'status {response.status_code}')

    def _headers(self):
        pass

    def _body(self):
        pass

    def _json(self, response):
        pass

    def _get_data(self, **args):
        pass