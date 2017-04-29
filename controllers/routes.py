from json import dumps
from falcon import HTTPNotFound
from data.utils import request
from data.constants import routes_url

__all__ = ['Routes', 'SingleRoute']

def get_routes():
    return request(routes_url)

class Routes:
    def on_get(self, request, response):
        """Routes route for the application"""
        data = get_routes()
        response.body = dumps(data)

class SingleRoute:
    def on_get(self, request, response, id):
        """Single route route for the application"""
        data = get_routes()
        found = None
        for route in data:
            if int(route['id']) == int(id):
                found = route
        if not found:
            raise HTTPNotFound(description="Route not found")
        response.body = dumps(found)
