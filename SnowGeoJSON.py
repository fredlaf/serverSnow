
from Geometry import Geometry
from Properties import Properties

class Snow:

    def __init__(self, type=None, stationName=None, snowQty=None, coordinates=None, date=None):
        self.geometry = Geometry(type, coordinates) # type is string, coordinates are array [lat, lon]
        self.properties = Properties(stationName, snowQty, date) # sName is string, snowQty is float, date is date.

    def jdefault(self):
        return self.geometry.to_json(), self.properties.to_json()

    def merge_two_dicts(self, x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z

    def printSnow(self):
        print("type: " + self.geometry.getType() +
                "name: " + self.properties.getName() +
              " snowQty: " + str(self.properties.getSnowQty()) +
              " date: " + str(self.properties.getDate()) +
              " geometry: " + str(self.geometry.getCoordinates()))


    def getGeometry(self):
        return self.geometry

    def getProperties(self):
        return self.properties

    def setGeometry(self, value):
        self.geometry = value

    def setProperties(self, value):
        self.properties = value

