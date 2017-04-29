from json import dumps
from falcon import HTTPNotFound
from data.utils import request
from data.constants import stop_lines_url, single_stop_lines_url

__all__ = ['ETA', 'SingleETA']


def get_eta():
    return request(stop_lines_url)


def get_single_eta(id):
    return request(single_stop_lines_url.format(stop_id=id))


class ETA:
    def on_get(self, request, response):
        """ETA route for the application"""
        data = get_eta()
        response.body = dumps(data)


class SingleETA:
    def on_get(self, request, response, id):
        """Single ETA route for the application"""
        data = get_single_eta(id)
        response.body = dumps(data)
