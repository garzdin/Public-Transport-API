from falcon import API
from googlemaps import Client
from controllers.index import *
from controllers.routes import *
from controllers.stops import *
from controllers.lines import *
from controllers.time_of_arrival import *
from controllers.times import *
from controllers.plan import *
from controllers.geocode import *

client = Client('AIzaSyAyFldhscDM2lrqaaYtk-EDuWZpagwTPDU')

app = API()
app.add_route('/', Index())
app.add_route('/routes', Routes())
app.add_route('/routes/{id}', SingleRoute())
app.add_route('/stops', Stops())
app.add_route('/stops/{id}', SingleStop())
app.add_route('/lines', Lines())
app.add_route('/lines/{id}', SingleLine())
app.add_route('/eta', ETA())
app.add_route('/eta/{id}', SingleETA())
app.add_route('/times/{r_id}/{s_id}', Times())
app.add_route('/plan', Plan())
app.add_route('/geocode', Geocode(client))
