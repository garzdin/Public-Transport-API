from json import dumps
from falcon import HTTPNotFound
from data.utils import request
from data.constants import stops_url

__all__ = ['Stops', 'SingleStop']


def get_stops():
    return request(stops_url)


class Stops:
    def on_get(self, request, response):
        """Stops route for the application"""
        data = get_stops()
        response.body = dumps(data)


class SingleStop:
    def on_get(self, request, response, id):
        """Single stop route for the application"""
        data = get_stops()
        found = None
        for stop in data:
            if int(stop['id']) == int(id):
                found = stop
        if not found:
            raise HTTPNotFound(description="Stop not found")
        response.body = dumps(found)
