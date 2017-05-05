from json import dumps

__all__ = ['Geocode']


class Geocode:
    def __init__(self, client, *args, **kwargs):
        self.client = client
        super(Geocode, self).__init__(*args, **kwargs)

    def on_get(self, request, response):
        """Geocode route for the application"""
        address = request.get_param('address') or ''
        google_response = self.client.geocode(address=address, components={'country': 'BG'}, language='bg')
        response.body = dumps(google_response)
