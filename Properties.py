
class Properties :

    def __init__(self, name=None, snowQty=None, date=None):
        self.name = name
        self.snowQty = snowQty
        self.date = date

    def jdefault(self):
        return self.__dict__

    def to_json(self):  # New special method.
        return {'properties': {'name': self.name, 'snowQty': self.snowQty, 'date': self.date}}

    def getName(self):
        return self.date

    def getSnowQty(self):
        return self.snowQty

    def getDate(self):
        return self.date