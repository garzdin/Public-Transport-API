from falcon import API
from controllers.index import *
from controllers.routes import *
from controllers.stops import *

app = API()
app.add_route('/', Index())
app.add_route('/routes', Routes())
app.add_route('/routes/{id}', SingleRoute())
app.add_route('/stops', Stops())
app.add_route('/stops/{id}', SingleStop())
