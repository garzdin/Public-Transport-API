from json import dumps
from falcon import HTTPNotFound
from data.utils import request
from data.constants import stop_times_url

__all__ = ['Times']


def get_times(r_id, s_id):
    return request(stop_times_url.format(route_id=r_id, stop_id=s_id))


class Times:
    def on_get(self, request, response, r_id=None, s_id=None):
        """Times route for the application"""
        data = get_times(r_id, s_id)
        response.body = dumps(data)
