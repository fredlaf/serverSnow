# By frederick Lafrance
# 2017-04-17
#
# Laval University, 2017

from Geometry import Geometry
from Properties import Properties

class Snow:

    def __init__(self, stationName=None, snowQty=None, latitude=None, longitude=None, date=None):
        self.stationName = stationName
        self.snowQty = snowQty
        self.latitude = latitude
        self.longitude = longitude
        self.date = date

    def jdefault(self):
        return self.__dict__

    def printSnow(self):
        print("name: " + self.stationName +
              " snowQty: " + str(self.snowQty) +
              " latitude: " + str(self.latitude) +
              " longitude: " + str(self.longitude) +
              " date: " + self.date)

    def getStationName(self):
        return self.stationName

    def getSnowQty(self):
        return self.snowQty

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getDate(self):
        return self.date

    def setStationName(self, value):
        self.stationName = value

    def setSnowQty(self, value):
        self.snowQty = value

    def setLatitude(self, value):
        self.latitude= value

    def setLongitude(self, value):
        self.longitude= value

    def setDate(self, value):
        self.date= value

