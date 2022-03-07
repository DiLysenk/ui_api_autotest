import requests
from enum import Enum
from component_api.logger import Logger


class Method(Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5


class MyRequests:

    @staticmethod
    def request_get(url, params: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, params, headers, cookies, Method.GET)

    @staticmethod
    def request_post(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.POST)

    @staticmethod
    def request_put(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.PUT)

    @staticmethod
    def request_patch(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.PATCH)

    @staticmethod
    def request_delete(url, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, Method.DELETE)

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method):
        url = f"{url}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)
        if method == Method.GET:
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == Method.POST:
            response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == Method.PUT:
            response = requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == Method.PATCH:
            response = requests.patch(url, data=data, headers=headers, cookies=cookies)
        elif method == Method.DELETE:
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)
        Logger.add_response(response)

        return response
