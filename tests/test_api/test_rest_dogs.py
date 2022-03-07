import cerberus
import pytest
from deepdiff import DeepDiff
from jsonschema import validate
from component_api.my_requests import MyRequests

class TestApi:
    def test_dog_api_status(self, response_get):
        assert response_get.status_code == 200

    def test_dog_api_include_success(self, response_get):
        assert "success" in response_get.json().get('status')

    @pytest.mark.parametrize("end_point", ['https://dog.ceo/api/breeds/list/all'])
    def test_dog_api_schema(self, response_get, end_point):
        schema = {
            "type": "object",
            'properties': {
                'message': {"type": "object"},
                'status': {"type": "string"},
            },
            'required': ['status'],
            'maxProperties': 2
        }
        validate(instance=response_get.json(), schema=schema)

    @pytest.mark.parametrize("end_point", ['https://dog.ceo/api/breeds/list/all'])
    def test_dog_api_schema_cerebrus(self, response_get, end_point):
        schema_c = {
            'message': {'type': 'dict'},
            'status': {'type': 'string', }
        }
        v = cerberus.Validator()
        assert v.validate(response_get.json(), schema_c)

    @pytest.mark.parametrize("end_point", ['https://dog.ceo/api/breeds/list/all'])
    def test_dog_api_data(self, response_get, end_point):
        expected_result = {
            'message': '',
            'status': 'success'
        }
        diff = DeepDiff(expected_result, response_get.json(), exclude_paths="root['message']")
        print(diff.pretty())
        assert not diff, diff.pretty()
