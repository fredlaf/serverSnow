# By frederick Lafrance
# 2017-04-17
#
# Laval University, 2017

import csv
import json
import csv
import io
import urllib.request

import pprint
from collections import defaultdict
import os
import psycopg2
from geojson import FeatureCollection

from Snow import Snow
# from SnowGeoJSON import Snow
from Connection import Connection
from geojson import Feature, Polygon
from Geometry import Geometry
from Properties import Properties

import flask

# Set the working directory to current directory.
# os.chdir('c:\\Users\\frederick\OneDrive - Universite Laval\maitrise\GMT7004_RealisationApplicationsSIG\webApps\ws')
# Telling which directory is the working one.

#Load CSV file and return a list string list as row
# Process raw data from CSV into clean data ready to be inserted into DB
def loadCSVfromFile(date):
    processedData= []
    fileName = "fre-climate-summaries-Québec-1,%s.csv" % (date)
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        count=0
        for row in reader:
            # Skip header.
            if count >= 32:
                tempLine = []
                # Start recovering values
                stationName = row[0]
                # Remplace comma with dot in string, and convert to float
                latitude = float((row[1]).replace(',', '.'))
                longitude = float((row[2]).replace(',', '.'))
                # if null, convert it to 0.
                if row[11] == '':
                    snowDrop = 0.0
                else:
                    snowDrop = float((row[11]).replace(',', '.'))
                # Fill data into tempList
                tempLine.append(stationName)
                tempLine.append(latitude)
                tempLine.append(longitude)
                tempLine.append(snowDrop)
                # print(tempLine)
                processedData.append(tempLine)
            count += 1
    print("-> Process for date : " + date + " completed!")
    return processedData

# Get data from Environment Canada Server given a start year (ex. 1950) and a end year (ex. 2016)
def getDataFromServer(startYear, endYear):
    for year in range(startYear, endYear):
        count = 0
        for month in range(1, 13):
            dataSet = []

            #Prepare URL to get data from.
            url = 'http://climat.meteo.gc.ca/prods_servs/cdn_climate_summary_report_f.html?intYear={0}&intMonth={1}&prov=QC&dataFormat=csv&btnSubmit=T%C3%A9l%C3%A9charger+des+donn%C3%A9es'.format(year, month)
            #print(url)

            #Get response from url.
            response = urllib.request.urlopen(url)

            #Read csv file.
            datareader = csv.reader(io.TextIOWrapper(response))
            print("Year : " + str(year) + "month : " + str(month) + " recovered!")

            #Create temp list
            tempList= list(datareader)

            count = 0
            #Skip header in list, append only dataset
            for row in tempList:
                if (count > 31):
                    dataSet.append(row)
                count += 1

            #insert data into database
            insertData(dataSet, year, month)

    # print elements in dataset
    # for element in dataSet:
    #     print(element)

# Enter your database info connection.
def getConnection():
    connection = Connection("localhost", "snow", "postgres", "postgres").getConnection()
    return connection

# Delete ALL data from database.
def deleteData():
    conn = getConnection()

    cursor = conn.cursor()

    preparedStatement = "DELETE FROM snow"

    try:
        cursor.execute(preparedStatement)
    except:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Insert data into database, given a date (YEAR and MONTH).
def insertData(data, year, month):
    # Establish a connection with DB.
    conn = getConnection()
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    try:
        for row in data:
            stationName= row[0]

            latitude = float((row[1]).replace(',', '.'))
            longitude = float((row[2]).replace(',', '.'))

            latlon = "POINT(" + str(latitude) + " " + str(longitude) + ")"

            precipitation= row[14]

            # if null, convert it to 0.
            if precipitation == '':
                precipitation = 0.0
            else:
                precipitation = float((precipitation.replace(',', '.')))

            #If month is below 10, a 0 must be added before the month. ex. 5 become 05
            if (month < 10):
                date = str(year) + '-' + '0' + str(month) + '-' + '1'

            else:
                date = str(year) + '-' + str(month) + '-' + '1'

            preparedStatement= "INSERT INTO snow (stationName, snowDrop, coordinates, date) VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s)"

            data= (stationName, precipitation, latlon, date)

            # Execute the statement
            cursor.execute(preparedStatement, data)

            print("++ Insert for date : " + date + " completed!")
    except:
        conn.rollback()
        raise #re-raise the last exception
    else:
        # Commit the transaction
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Recover data from database, given the date and the type of data to recover.
def recoverData(date, type):

    conn = getConnection()

    cursor = conn.cursor()

    snowObjects = []
    featuresList = []
    aFeatureCollection = None
    if (type == "point"):
        cursor.execute(
            "select stationname, snowdrop, st_y(coordinates) as lat, st_x(coordinates) as lon, to_char(date, 'YYYY-MM-DD') as date " +
            "from snow " +
            "where date = %s " +
            "group by stationname, snowDrop, st_x(coordinates), st_y(coordinates), date " +
            "order by stationname, date ", (date,))
        # "limit 100", (date,))


        # Retreive records from db.
        records = cursor.fetchall()
        # Construct a list of objects.
        aFeatureCollection= []
        for row in records:
            # If the value of snowQty is not equals to 0, append it to the list.
            if (row[1] != 0):
                # (self, stationName=None, snowQty=None, latitude=None, longitude=None, date=None):
                snowOB = Snow(row[0], row[1], row[2], row[3], row[4])
                # Add it to list.
                aFeatureCollection.append(snowOB)
    elif (type == "polygon"):
        cursor.execute(
            "select stationname, snowdrop, st_y(coordinates) as lat, st_x(coordinates) as lon, to_char(date, 'YYYY-MM-DD') as date " +
            "from snow " +
            "where date = %s " +
            "group by stationname, snowDrop, st_x(coordinates), st_y(coordinates), date " +
            "order by stationname, date "
            "limit 100", (date,))

        # Retreive records from db.
        records = cursor.fetchall()

        # Construct a geoJSON.
        for row in records:
            # If the value of snowQty is not equals to 0, append it to the list.
            if (row[1] != 0):
                # Construct a new geometry of type Polygon from point.
                # Make a BBox around the point.
                aPolygon = Polygon([[[row[2]+0.08, row[3]+0.05],
                           [row[2] - 0.08, row[3] + 0.05],
                           [row[2] - 0.08, row[3] - 0.05],
                           [row[2] + 0.08, row[3] - 0.05]]])


                # Create a feature from polygon.
                aFeature = Feature(geometry=aPolygon,
                                   properties={"name": row[0], "snowQty": row[1], "date": row[4]})

                # Add it to list.
                featuresList.append(aFeature)

                    # print(aFeatureCollection)
    elif (type == "ecity"):
        # TEMP for spatiotemporal simulation test.

        propositionPolygon1 = Polygon([[[-73.573458+0.0005, 45.505204+0.0003],
                           [-73.573458 - 0.0005, 45.505204 + 0.0003],
                           [-73.573458 - 0.0005, 45.505204 - 0.0003],
                           [-73.573458 + 0.0005, 45.505204 - 0.0003]]]) #+-

        proposition1 = Feature(geometry=propositionPolygon1, properties={"name": "Bus en retard","popularity": 50, "date": "2017-03-28"})
        featuresList.append(proposition1)

        propositionPolygon2 = Polygon([[[-73.574764+0.0005,45.503526+0.0003],
                           [-73.574764 - 0.0005, 45.503526 + 0.0003],
                           [-73.574764 - 0.0005, 45.503526 - 0.0003],
                           [-73.574764 + 0.0005, 45.503526 - 0.0003]]])

        proposition2 = Feature(geometry=propositionPolygon2,
                           properties={"name": "service mediocre", "popularity": 30, "date": "2017-04-01"})
        featuresList.append(proposition2)

        propositionPolygon3 = Polygon([[[-73.565411+0.0005, 45.500301+0.0003],
                           [-73.565411 - 0.0005, 45.500301 + 0.0003],
                           [-73.565411 - 0.0005, 45.500301 - 0.0003],
                           [-73.565411 + 0.0005, 45.500301 - 0.0003]]])

        # Create a feature from polygon.
        proposition3 = Feature(geometry=propositionPolygon3,
                           properties={"name": "temps attente transport en commun", "popularity": 80, "date": "2017-03-27"})


        # Add it to list.
        featuresList.append(proposition3)

    # Construct FeatureCollection
    aFeatureCollection = FeatureCollection(featuresList)

    print(aFeatureCollection)
    return aFeatureCollection

# Convert list to json, and return a json string.
def fromListToJson(list):
    snowOB = Snow()
    #Doit transformer en dict puis en JSON.
    json_string = json.dumps([snowOB.__dict__ for snowOB in list])
    # Print JSON for testing.
    print(json_string)
    # Return json.
    return json_string

# Process and insert all data.
def processInserting(dateBegin, dateEnd):
    if __name__ == '__main__':
        for date in range(dateBegin, dateEnd):
            # Load and process all data from csv file.
            rawData = loadCSVfromFile(str(date))

            # Format date into a readable foramt for database.
            dateFormat = str(date) + '-01'+'-01'

            # insert data into db.
            insertData(rawData, dateFormat)

#for testing only.
# getDataFromServer(1950, 2016)
