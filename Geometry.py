import geojson

class Geometry :

    def __init__(self, type=None, coordinates=None):
        self.type = type
        self.coordinates = coordinates

    def jdefault(self):
        return self.__dict__

    @property
    def __geo_inteface__(self):  # New special method.
        return {'geometry': {'type': 'Polygon', 'coordinates': self.coordinates}}

    def getType(self):
        return self.type

    def getCoordinates(self):
        return self.coordinates