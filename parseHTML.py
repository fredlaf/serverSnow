# By frederick Lafrance
# 2017-04-17
#
# Laval University, 2017

import csv
import io
import urllib.request

response = urllib.request.urlopen('http://climat.meteo.gc.ca/prods_servs/cdn_climate_summary_report_f.html?intYear=2012&intMonth=7&prov=QC&dataFormat=csv&btnSubmit=T%C3%A9l%C3%A9charger+des+donn%C3%A9es')
datareader = csv.reader(io.TextIOWrapper(response))

count = 0

dataSet = list(datareader)

#Skip header in list, append only dataset
for row in dataSet:
    if (count > 31):
        print(row[1])
    count += 1

# for row in datareader:
#     if (count > 31):
#         dataSet.append(row)
#         # print(row)
#     count+=1
#
# for element in dataSet:
#     print(element[2])