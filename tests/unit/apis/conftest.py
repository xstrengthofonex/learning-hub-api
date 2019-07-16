from aiohttp import web
from asynctest import Mock


def create_mock_request(data):
    mock_request = Mock(web.Request)
    mock_request.json.return_value = data
    return mock_request
