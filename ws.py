import flask
from flask import Flask, request, Response
import ProcessData
import json

app = Flask(__name__)

# Default URL. return 'hello world' page.
@app.route('/')
def hello_world():
    return 'Hello World!'

# Mapping URL /getDataGeoJSON, accessing it by POST method.
# Return geoJSON containing all snow features according to given date.
@app.route('/getData', methods=['POST'])
def getData():
    if request.method == 'POST':
        date = request.form['date']
        type = request.form['type']
        date = "%s-01-01" % date
        # todo add a method to build a geoJson.
        snowGeoJson= None
        if (type == 'polygon'):
            snowGeoJson = ProcessData.recoverData(date, type)
            snowGeoJson = json.dumps(snowGeoJson)
        elif (type == 'point'):
            objList = ProcessData.recoverData(date, type)
            snowGeoJson = ProcessData.fromListToJson(objList)
        # Setting a response with json and header.
        response = Response(snowGeoJson, mimetype='application/json')
        # Adding ACAO to response header for security purpose, so it can match the header of client.
        response.headers.add('Access-Control-Allow-Origin', '*')

        # print(response.get_data())
        return response
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return 'failed'

@app.after_request
def after(response):
  # todo with response
  print(response.status)
  print(response.headers)
  print(response.get_data())
  return response


if __name__ == '__main__':
    app.run()
