import requests
from enum import Enum


class Method(Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5


class MyRequests:

    @staticmethod
    def get(url, params: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, params, headers, cookies, Method.GET)

    @staticmethod
    def post(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.POST)

    @staticmethod
    def put(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.PUT)

    @staticmethod
    def patch(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.PATCH)

    @staticmethod
    def delete(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.DELETE)

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method):
        url = f"http://{url}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        if method == Method.GET:
            return requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == Method.POST:
            return requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == Method.PUT:
            return requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == Method.PATCH:
            return requests.patch(url, data=data, headers=headers, cookies=cookies)
        elif method == Method.DELETE:
            return requests.delete(url, data=data, headers=headers, cookies=cookies)
