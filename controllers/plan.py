from json import load, dumps
from falcon import HTTPBadRequest
from data.constants import stops_url
from data.utils import request, haversine
from data.models import *
from data.serializers import *

__all__ = ['Plan']

def _get_stops():
    data = request(stops_url)

    stops = {}

    for stop in data:
        id = stop['id']
        name = stop['name']
        coordinates = Coordinates(stop['lat'], stop['lon'])
        stops[id] = Stop(id, name, coordinates)

    return stops

def _find_closest(origin, stops):
    return min(stops, key=lambda s: haversine(stops[s].coordinates.__dict__.values(), origin.__dict__.values()))


class Plan:
    def on_post(self, request, response):
        """Plan route for the application"""
        try:
            data = load(request.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'start' not in data or 'end' not in data:
            raise HTTPBadRequest(
                description="Provide a start and an end coordinate")
        if 'latitude' not in data['start'] or 'longitude' not in data['start'] or 'latitude' not in data['end'] or 'longitude' not in data['end']:
            raise HTTPBadRequest(
                description="Provide all fields for start and an end coordinates")
        start = Coordinates(**data['start'])
        end = Coordinates(**data['end'])
        stops = _get_stops()
        start_stop = _find_closest(start, stops)
        end_stop = _find_closest(end, stops)
        path = Path(start_stop, end_stop, stops)
        response.body = dumps(path.find(), cls=ClassEncoder)
