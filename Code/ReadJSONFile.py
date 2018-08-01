import json
import csv

json_data = open('OriginalClusterImportCPU').read()
json_parsed = json.loads(json_data)


cpu_data = json_parsed['Datapoints']



# open a file for writing
parsed_data = open('ClusterImportCPU.csv', 'w')


# create the csv writer object
csvwriter = csv.writer(parsed_data)
count = 0
for record in parsed_data:
    if count == 0:
        header = record.keys()
        csvwriter.writerrow(header)
        count += 1
    csvwriter.writerrow(record.values())
parsed_data.close()