from json import JSONDecodeError

from requests import Response


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'отсутствует cookie {cookie_name}'
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.cookies, f'отсутствует headers {headers_name}'
        return response.headers[headers_name]

    def get_json(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f'в запросе отсутствует json {response.text}'
        assert name in response_as_dict, f'Отсутствует ключ {name}'
        return response_as_dict[name]

    def get_status(self, response):
        assert response.status_code != 500, f'status is {response.status_code}'