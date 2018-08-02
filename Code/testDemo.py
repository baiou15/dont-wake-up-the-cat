import os
import time
import datetime
import json
import boto3

class demoFunction():
    def __init__(self, status, metric_name):
        self.status = status
        self.metric_name = metric_name

    def pushToS3(bucket, key, json):
        s3 = boto3.client('s3', region_name='us-east-1')
        response = s3.put_object(
            Body=bytes(str(json), encoding="UTF-8"),
            Bucket=bucket,
            Key=key,
        )

    def getDataFile(self):
        (startTime, endTime) = self.getTime()
        # filename = "S3UploadDisk.txt"
        # f = open(filename, "w+")
        # commandLine = 'aws cloudwatch get-metric-statistics --namespace CWAgent --metric-name disk_used_percent --dimensions --dimensions Name=InstanceId,Value=i-028ddedc7959823db Name=path,Value=/ Name=device,Value=nvme0n1p1 Name=fstype,Value=ext4 --statistics Maximum --start-time ' + startTime + ' --end-time '+endTime+' --period 300 --profile eabprod'

        commandLines = [
            ('CPU',
             'aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=',
             ' --statistics Maximum --start-time ', ' --end-time ', ' --period 300 --profile eabprod'),
            ('Disk',
             'aws cloudwatch get-metric-statistics --namespace CWAgent --metric-name disk_used_percent --dimensions Name=InstanceId,Value=',
             ' Name=path,Value=/ Name=device,Value=nvme0n1p1 Name=fstype,Value=ext4 --statistics Maximum --start-time ', ' --end-time ', ' --period 300 --profile eabprod'),
            ('Memory',
             'aws cloudwatch get-metric-statistics --namespace CWAgent --metric-name mem_used_percent --dimensions Name=InstanceId,Value=',
             ' --statistics Maximum --start-time ', ' --end-time ', ' --period 300 --profile eabprod'),
            ('aws cloudwatch get-metric-statistics --namespace EAB/panto --metric-name ', ' --dimensions Name=Status,Value=',
             ' --statistics Maximum --start-time ', ' --end-time ', ' --period 300 --profile eabprod')
        ]

        instances = [('clusterImport', 'i-081ce81b0d81cebc6'),
                     ('metadataGeneration', 'i-0cc04718067179871'),
                     ('s3Upload', 'i-028ddedc7959823db')]

        s3Statuses = ["00_10_3_RELOAD_FROM_S3", "30_10_1_S3_DOWNLOAD_START"]
        metadataStatus = ["40_00_1_S3_TEMP_FILE_DOWNLOAD_START",
                    "40_00_5_S3_TEMP_FILE_DOWNLOAD_SUCCESS", "40_10_1_METADATA_GENERATION_START",
                    "40_10_5_METADATA_GENERATION_SUCCESS", "40_12_1_S3_TEMP_FILE_DOWNLOAD_START",
                    "40_12_5_S3_TEMP_FILE_DOWNLOAD_SUCCESS", "40_14_5_ADDING_CONSTANTS_STEP_SUCCESS",
                    "40_20_1_FILE_TRANSFORMATION_START", "40_20_5_FILE_TRANSFORMATION_SUCCESS",
                    "40_30_1_S3_TEMP_FILE_UPLOAD_START"]
        clusterImportStatus = ["40_30_5_S3_TEMP_FILE_UPLOAD_SUCCESS", "50_05_1_S3_TEMP_FILE_DOWNLOAD_START",
                    "50_05_5_S3_TEMP_FILE_DOWNLOAD_SUCCESS", "50_10_1_UPLOAD_HDFS_CREATE_HDFS_DIR_START",
                    "50_10_5_UPLOAD_HDFS_CREATE_HDFS_DIR_SUCCESS", "50_20_1_UPLOAD_HDFS_HDFS_MOVE_START",
                    "50_20_5_UPLOAD_HDFS_HDFS_MOVE_SUCCESS", "50_30_0_1_UPLOAD_HDFS_CLEAN_LOCAL_COPY_START",
                    "50_30_0_5_UPLOAD_HDFS_CLEAN_LOCAL_COPY_SUCCESS",
                    "50_40_0_1_UPLOAD_HDFS_FILETYPE_PROCESSING_RULE_START",
                    "50_40_0_5_UPLOAD_HDFS_FILETYPE_PROCESSING_RULE_SUCCESS", "60_10_1_HIVE_TABLE_CREATE_START",
                    "60_10_5_HIVE_TABLE_CREATE_SUCCESS", "60_20_1_HIVE_TABLE_CREATE_TEMP_TABLE_START",
                    "60_20_5_HIVE_TABLE_CREATE_TEMP_TABLE_SUCCESS", "70_10_1_HIVE_TABLE_ADD_PARTITION_START",
                    "70_10_5_HIVE_TABLE_ADD_PARTITION_SUCCESS", "80_10_1_COPY_TO_ORC_START",
                    "80_10_5_COPY_TO_ORC_SUCCESS", "80_20_1_CLEAN_TEMP_TABLE_START"]
        metric_names = ['Backlog', 'Velocity-T1', 'Velocity-T2']

        self.saveToFile(startTime, endTime, commandLines, s3Statuses, metric_names, instances, 0)
        self.saveToFile(startTime, endTime, commandLines, metadataStatus, metric_names, instances, 1)
        self.saveToFile(startTime, endTime, commandLines, clusterImportStatus, metric_names, instances, 2)


    def getTime(self):
        startDate = (datetime.datetime.now()-datetime.timedelta(minutes=30)).strftime("%Y-%m-%d")
        startTimeStamp = 'T' + (datetime.datetime.now()-datetime.timedelta(minutes=30)).strftime('%H:%M:%S')
        startTime = startDate + startTimeStamp
        endDate = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        endTimeStamp = 'T' + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        endTime = endDate + endTimeStamp
        return startTime, endTime

    def saveToFile(self, startTime, endTime, commandLines, statuses, metrics, instances, instanceNum):
        columnnames = 'Metrics-Timestamp,'
        alldata = {}
        index = 0
        for status in statuses:
            for metric_name in metrics:
                commandInfo = commandLines[3]
                commandLine = commandInfo[0] + metric_name + commandInfo[1] + status + commandInfo[2] + startTime + \
                              commandInfo[3] + endTime + commandInfo[4]
                serviceData = os.popen(commandLine)
                fileName = status + "-" + metric_name
                print('Now working on ', fileName)
                nameparts = fileName.split('-')
                subnameparts = nameparts[0].split("_")
                columnprefix = ''
                if len(nameparts) > 1:
                    columnprefix = nameparts[len(nameparts) - 1] + '-' + subnameparts[0] + '-' + subnameparts[1] + '-' + \
                                   subnameparts[2] + '-' + subnameparts[3]
                else:
                    columnprefix = fileName
                data = json.load(serviceData)
                datapoints = data['Datapoints']
                for datapoint in datapoints:
                    timestamp = datapoint['Timestamp']
                    if timestamp in alldata:
                        alldata[timestamp] += ',' + str(datapoint['Maximum'])
                    else:
                        alldata[timestamp] = (',' * index) + str(datapoint['Maximum'])
                for key, value in alldata.items():
                    append_count = index - value.count(',')
                    alldata[key] = value + (',' * append_count)
                columnnames += columnprefix + ','
                index = index + 1
                if len(statuses) > 2:
                    if metric_name == 'Velocity-T2':
                        for key, value in alldata.items():
                            accelerateCal = alldata[key].split(',')
                            alldata[key] = alldata[key] + ',' + str(float(accelerateCal[-2]) - float(accelerateCal[-1]))
                            columnnames += 'Acceleration' + ','
                # f.write(test)
                # f.close()

        for i in range(3):
            item = instances[instanceNum]
            instanceId = item[1]
            instanceName = item[0]
            commandInfo = commandLines[i]
            commandLine = commandInfo[1] + instanceId + commandInfo[2] + startTime + commandInfo[3] + endTime + \
                          commandInfo[4]
            columnprefix = instanceName + commandInfo[0]
            print('Now working on ', columnprefix)
            serviceData = os.popen(commandLine)
            data = json.load(serviceData)
            datapoints = data['Datapoints']
            for datapoint in datapoints:
                timestamp = datapoint['Timestamp']
                if timestamp in alldata:
                    alldata[timestamp] += ',' + str(datapoint['Maximum'])
                else:
                    alldata[timestamp] = (',' * index) + str(datapoint['Maximum'])
            for key, value in alldata.items():
                append_count = index - value.count(',')
                alldata[key] = value + (',' * append_count)
            columnnames += columnprefix + ','
            index = index + 1
        fout = "/Users/baio/dev/projects/dont-wake-up-the-cat/" + instanceName + "Result.csv"
        fo = open(fout, "w")

        fo.write(columnnames + "\n");
        for k, v in alldata.items():
            fo.write(str(k) + ',' + str(v) + '\n')

        fo.close()


test = demoFunction('','')
test.getDataFile()
