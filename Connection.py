# By frederick Lafrance
# 2017-04-17
#
# Laval University, 2017

import psycopg2

class Connection:

    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection_string = "host=%s dbname=%s user=%s password=%s" % (self.host,
                                                                            self.dbname,
                                                                            self.user,
                                                                            self.password)

    def getHost(self):
        return str(self.host)

    def getDBname(self):
        return str(self.dbname)

    def getPassword(self):
        return str(self.password)

    def getUser(self):
        return str(self.user)

    def getConnection(self):
        try:
            conn = psycopg2.connect(self.connection_string)
            print("Connected!\n")
            return conn
        except:
            print("Connection failed!")
            raise


