import requests


class Get:

    def __init__(self, url):
        self.url = url

    def get(self, url):
        return requests.get(url)

    def _body(self):
        return

    def _headers(self):
        return
