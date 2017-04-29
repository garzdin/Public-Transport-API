from json import load, dumps
from falcon import HTTPBadRequest
from data.models import *
from data.serializers import *

__all__ = ['Plan']


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
        path = Path(1909, 1882) # TODO: Find the nearest stops to start and and
        response.body = dumps(path.find(), cls=ClassEncoder)
