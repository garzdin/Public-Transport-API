from falcon import API
from controllers.index import *
from controllers.routes import *
from controllers.stops import *
from controllers.lines import *

app = API()
app.add_route('/', Index())
app.add_route('/routes', Routes())
app.add_route('/routes/{id}', SingleRoute())
app.add_route('/stops', Stops())
app.add_route('/stops/{id}', SingleStop())
app.add_route('/lines', Lines())
app.add_route('/lines/{id}', SingleLine())
