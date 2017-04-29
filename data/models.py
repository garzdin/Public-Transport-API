from .constants import *
from .utils import *
from .serializers import *

__all__ = ['Graph', 'Coordinates', 'Stop', 'Route', 'Path']


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
    def __init__(self, id, name, coordinates, line=None, route=None):
        self.id = id
        self.line = line
        self.route = route
        self.name = name
        self.coordinates = coordinates

    @property
    def info(self):
        from json import dumps

        data = request(single_stop_lines_url.format(stop_id=self.id))

        info = []

        for stop in data:
            info.append({
                'id': stop['stopId'],
                'line': stop['lineId'],
                'route': stop['routeId'],
                'arrives_in': stop['remainingTime']
            })

        return dumps(info)

    def at_line(line_id):
        from json import dumps

        data = request(single_stop_lines_url.format(stop_id=self.id))

        for stop in data:
            if stop['line'] == line_id:
                return dumps({
                    'id': stop['stopId'],
                    'line': stop['lineId'],
                    'route': stop['routeId'],
                    'arrives_in': stop['remainingTime']
                })

        return dumps({})

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.coordinates == other.coordinates

    def __str__(self):
        string = "Id: " + str(self.id) + "\n"
        string += "Name: " + str(self.name.encode('utf-8')) + "\n"
        string += "Coordinates: " + str(self.coordinates)
        return string


class Route:
    def __init__(self, id, line, stops):
        self.id = id
        self.line = line
        self.stops = stops

    def __eq__(self, other):
        return self.id == other.id and self.line == other.line and self.stops == other.stops

    def __str__(self):
        string = "Id: " + str(self.id) + "\n"
        string += "Line: " + str(self.line) + "\n"
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
            line = route['lineId']
            stops = []
            for stop_id in route['stopIds']:
                self.stops[stop_id].route = id
                self.stops[stop_id].line = line
                stops.append(self.stops[stop_id])
            routes[id] = Route(id, line, stops)

        return routes

    def _create_graph(self):
        graph = Graph()

        stop_times = request(stop_lines_url)

        for route in self.routes.values():
            for stop in route.stops:
                time_to_wait = 0.0
                arrives_in = []
                for line in stop_times:
                    if line['remainingTime'] and line['stopId'] == stop.id and line['lineId'] == route.line:
                        for time in line['remainingTime']:
                            arrives_in.append(time)
                if arrives_in:
                    time_to_wait = sum(arrives_in) / 10000.0
                graph.add_vertex(stop.id)
                edges = 0.0
                for vertex_stop in route.stops:
                    if vertex_stop not in [stop]:
                        edges += 0.1
                        distance = stop.coordinates.distance(vertex_stop.coordinates)
                        graph.add_edge(stop.id, vertex_stop.id, (distance + time_to_wait + edges))

        return graph

    def find(self):
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
