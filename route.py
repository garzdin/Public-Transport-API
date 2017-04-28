session_id_key = 'eurogps.eu.sid'
session_id = '0e8f8d7a4cc333e2bbbf1b8f64bf4aae5cffc45b1ce44795'
stops_url = 'http://gtpl.asti.eurogps.eu:8080/rest-its/scheme/stops'
routes_url = 'http://gtpl.asti.eurogps.eu:8080/rest-its/scheme/routes'
stop_line_url = 'http://gtpl.asti.eurogps.eu:8080/rest-its/scheme/stop-lines/{stop_id}'

def seconds_to_minutes(seconds):
    from time import strftime, gmtime

    return "{minutes} minutes".format(minutes=strftime("%M:%S", gmtime(seconds)))

def request(url):
    from urllib2 import Request, urlopen
    from json import loads

    headers = {}

    headers[session_id_key] = session_id

    request = Request(url, headers=headers)

    response = urlopen(request).read()
    return loads(response)


class Graph:
    def __init__(self):
        from collections import defaultdict

        self.vertices = set()
        self.edges = defaultdict(list)
        self.weights = {}

    def __eq__(self, other):
        return self.vertices == other.vertices and self.edges == other.edgest and self.weights == other.weights

    def __str__(self):
        string = "Vertices: " + str(self.vertices) + "\n"
        string += "Edges: " + str(self.edges) + "\n"
        string += "Weights: " + str(self.weights)
        return string

    def add_vertex(self, value):
        self.vertices.add(value)

    def add_edge(self, from_vertex, to_vertex, distance):
        if from_vertex == to_vertex: pass
        self.edges[from_vertex].append(to_vertex)
        self.weights[(from_vertex, to_vertex)] = distance


class Coordinates:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __str__(self):
        string = "Latitude: " + str(self.latitude) + "\n"
        string += "Longitude: " + str(self.longitude)
        return string

    def distance(self, other):
        from math import radians, cos, sin, asin, sqrt

        longitude_one, latitude_one, longitude_two, latitude_two = map(radians, [self.longitude, self.latitude, other.longitude, other.latitude])
        longitude_difference = longitude_two - longitude_one
        latitude_difference = latitude_two - latitude_one
        angle = sin(latitude_difference / 2) ** 2 + cos(latitude_one) * cos(latitude_two) * sin(longitude_difference / 2) ** 2
        circumference = 2 * asin(sqrt(angle))
        radius = 6371
        return circumference * radius


class Stop:
    def __init__(self, id, name, coordinates):
        self.id = id
        self.name = name
        self.coordinates = coordinates

    def __eq__(self, other):
        return self.id == other.id and self.coordinates == other.coordinates

    def get_info(self):
        data = request(stop_line_url.format(stop_id=self.id))

        info = []

        for stop in data:
            info.append({
                'id': stop['stopId'],
                'line': stop['lineId'],
                'route': stop['routeId'],
                'arrives_in': [seconds_to_minutes(seconds) for seconds in stop['remainingTime']]
            })

        return info

    def __str__(self):
        string = "Id: " + str(self.id) + "\n"
        string += "Name: " + str(self.name.encode('utf-8')) + "\n"
        string += "Coordinates: " + str(self.coordinates)
        return string

class Route:
    def __init__(self, id, stops):
        self.id = id
        self.stops = stops

    def __eq__(self, other):
        return self.id == other.id and self.stops == other.stops

    def __str__(self):
        string = "Id: " + str(self.id) + "\n"
        string += "Stops: " + str(self.stops)
        return string



class Path:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.stops = self._get_stops()
        self.routes = self._get_routes()
        self.graph = self._create_graph()

    def _get_stops(self):
        data = request(stops_url)

        stops = {}

        for stop in data:
            id = stop['id']
            name = stop['name']
            coordinates = Coordinates(stop['lat'], stop['lon'])
            stops[id] = Stop(id, name, coordinates)

        return stops

    def _get_routes(self):
        data = request(routes_url)

        routes = {}

        for route in data:
            id = route['id']
            stops = []
            for stop_id in route['stopIds']:
                stops.append(self.stops[stop_id])
            routes[id] = Route(id, stops)

        return routes

    def _create_graph(self):
        graph = Graph()

        for route in self.routes.values():
            for stop in route.stops:
                graph.add_vertex(stop.id)
                for vertex_stop in route.stops:
                    if vertex_stop not in [stop]:
                        distance = stop.coordinates.distance(vertex_stop.coordinates)
                        graph.add_edge(stop.id, vertex_stop.id, distance)

        return graph

    def find_route(self):
        visited = set()

        delta = dict.fromkeys(list(self.graph.vertices), float("inf"))
        previous = dict.fromkeys(list(self.graph.vertices), None)

        delta[self.start] = 0

        while visited != self.graph.vertices:
            current = min((set(delta.keys()) - visited), key=delta.get)

            for neighbor in set(self.graph.edges[current]) - visited:
                new_path = delta[current] + self.graph.weights[current, neighbor]

                if new_path < delta[neighbor]:
                    delta[neighbor] = new_path
                    previous[neighbor] = current

            visited.add(current)

        path = []
        vertex = self.end

        while vertex is not None:
            path.append(self.stops[vertex])
            vertex = previous[vertex]

        path.reverse()
        return path

path = Path(1909, 1882)
for stop in path.find_route():
    print(stop.get_info())
