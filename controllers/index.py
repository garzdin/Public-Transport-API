from json import dumps

__all__ = ['Index']

class Index:
    def on_get(self, request, response):
        """Index route for the application"""
        message = {
            'message': "Public transport API for the city of Pleven, Bulgaria",
            'author': "Teodor Garzdin <teodorgarzedin@gmail.com>",
            'version': "1"
        }
        response.body = dumps(message)
