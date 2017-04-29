from falcon import API
from controllers import *

api = API()
api.add_route('/', Index())
