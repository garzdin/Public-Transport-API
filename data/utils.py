from math import radians, cos, sin, asin, sqrt

__all__ = ['seconds_to_minutes', 'request', 'haversine']

AVG_EARTH_RADIUS = 6371 # km

def seconds_to_minutes(seconds):
    from time import strftime, gmtime

    return "{minutes} minutes".format(minutes=strftime("%M:%S", gmtime(seconds)))

def request(url):
    try:
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
    except ModuleNotFoundError:
        from urllib2 import Request, urlopen
    except ModuleNotFoundError:
        from urllib3 import Request, urlopen
    from json import loads
    from .constants import session_id_key, session_id

    headers = {}

    headers[session_id_key] = session_id

    request = Request(url, headers=headers)

    try:
        response = urlopen(request).read()
    except HTTPError as e:
        return {
            'error': str(e),
            'message': str(e.read().decode("utf-8"))
        }
    else:
        return loads(response)


def haversine(point1, point2):
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))

    return h  # in kilometers
