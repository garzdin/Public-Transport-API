from json import dumps
from falcon import HTTPNotFound
from data.utils import request
from data.constants import lines_url

__all__ = ['Lines', 'SingleLine']


def get_lines():
    return request(lines_url)


class Lines:
    def on_get(self, request, response):
        """Lines route for the application"""
        data = get_lines()
        response.body = dumps(data)


class SingleLine:
    def on_get(self, request, response, id):
        """Single stop route for the application"""
        data = get_lines()
        found = None
        for stop in data:
            if int(stop['id']) == int(id):
                found = stop
        if not found:
            raise HTTPNotFound(description="Line not found")
        response.body = dumps(found)
