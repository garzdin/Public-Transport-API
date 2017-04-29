from falcon import API
from app.controllers import *

api = API()
api.add_route('/', Index())
