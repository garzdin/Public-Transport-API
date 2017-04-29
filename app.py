from falcon import API
from controllers.index import *

app = API()
app.add_route('/', Index())
