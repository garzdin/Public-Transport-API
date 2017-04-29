from falcon import API
from controllers.index import *
from controllers.routes import *

app = API()
app.add_route('/', Index())
app.add_route('/routes', Routes())
app.add_route('/routes/{id}', SingleRoute())
