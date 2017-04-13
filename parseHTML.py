import csv
import io
import urllib.request

response = urllib.request.urlopen('http://climat.meteo.gc.ca/prods_servs/cdn_climate_summary_report_f.html?intYear=2012&intMonth=7&prov=QC&dataFormat=csv&btnSubmit=T%C3%A9l%C3%A9charger+des+donn%C3%A9es')
datareader = csv.reader(io.TextIOWrapper(response))

for row in datareader:
    print(row)
