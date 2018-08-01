import json
import csv
from os import listdir
from os.path import isfile, join

# mypath='/Users/wangy/git/Hackathon-1/SampleData/';
mypath = '/Users/baio/dev/projects/dont-wake-up-the-cat/SampleData/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

alldata = {}
index = 0
columnnames = 'Metrics-Timestamp,'
for datafile in onlyfiles:
    print('Now working on %s', datafile)
    shortdatafile = datafile[:datafile.find(".")]
    nameparts = shortdatafile.split('-')
    columnprefix = ''
    if len(nameparts) > 1:
        columnprefix = nameparts[len(nameparts)-1] + '-' + nameparts[0].split('_')[0]
    else:
        columnprefix = datafile

    with open(mypath+datafile) as f:
        data = json.load(f)
        datapoints = data['Datapoints']
        for datapoint in datapoints:
            timestamp = datapoint['Timestamp']
            if timestamp in alldata:
                alldata[timestamp]+=','+str(datapoint['Maximum'])
            else:
                alldata[timestamp]= (','*index) + str(datapoint['Maximum'])
    for key, value in alldata.items():
        append_count = index - value.count(',')
        alldata[key] = value + (','*append_count)
    columnnames += columnprefix + '-Maximum,'
    index = index + 1
    # if (index == 2):
    #     break
    continue

#alldata will hold all the data
#columnnames will hold the column name list
fout = "/Users/baio/dev/projects/dont-wake-up-the-cat/result.csv"
fo = open(fout, "w")

fo.write(columnnames + "\n");
for k, v in alldata.items():
    fo.write(str(k) + ',' + str(v) + '\n')

fo.close()