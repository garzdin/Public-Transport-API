from falcon import API
from controllers.index import *

api = API()
api.add_route('/', Index())
