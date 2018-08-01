import os

class hackthonfunction():
    def __init__(self, status, metric_name):
        self.status = status
        self.metric_name = metric_name

    def getFile(self):
        startTime = 1
        filename = "/Users/baio/Documents/Projects/Python/Hackathon-1/SampleData/" + self.status + "-" + self.metric_name + ".txt"
        f = open(filename, "w+")
        for i in range(29):
            if i < 9:
                start = '0' + str(startTime+i)
                if i != 8:
                    end = '0' + str(startTime+ i + 1)
                else:
                    end = str(startTime + i + 1)
            else:
                start = str(startTime+i)
                end = str(startTime + i + 1)
            commandLine = 'aws cloudwatch get-metric-statistics --namespace EAB/panto --metric-name ' + self.metric_name + ' --dimensions Name=Status,Value=' + self.status + ' --statistics Maximum --start-time 2018-07-'+start+'T00:00:00 --end-time 2018-07-'+end+'T00:00:00 --period 300 --profile eabprod'
            print(commandLine)
            test = os.popen(commandLine).read()
            f.write(test)
        f.close()


statuses = ["30_10_1_S3_DOWNLOAD_START", "40_00_1_S3_TEMP_FILE_DOWNLOAD_START", "40_00_5_S3_TEMP_FILE_DOWNLOAD_SUCCESS", "40_10_1_METADATA_GENERATION_START", "40_10_5_METADATA_GENERATION_SUCCESS", "40_12_1_S3_TEMP_FILE_DOWNLOAD_START", "40_12_5_S3_TEMP_FILE_DOWNLOAD_SUCCESS", "40_14_5_ADDING_CONSTANTS_STEP_SUCCESS", "40_20_1_FILE_TRANSFORMATION_START", "40_20_5_FILE_TRANSFORMATION_SUCCESS", "40_30_1_S3_TEMP_FILE_UPLOAD_START", "40_30_5_S3_TEMP_FILE_UPLOAD_SUCCESS", "00_10_3_RELOAD_FROM_S3", "50_05_1_S3_TEMP_FILE_DOWNLOAD_START", "50_05_5_S3_TEMP_FILE_DOWNLOAD_SUCCESS", "50_10_1_UPLOAD_HDFS_CREATE_HDFS_DIR_START", "50_10_5_UPLOAD_HDFS_CREATE_HDFS_DIR_SUCCESS", "50_20_1_UPLOAD_HDFS_HDFS_MOVE_START", "50_20_5_UPLOAD_HDFS_HDFS_MOVE_SUCCESS", "50_30_0_1_UPLOAD_HDFS_CLEAN_LOCAL_COPY_START", "50_30_0_5_UPLOAD_HDFS_CLEAN_LOCAL_COPY_SUCCESS", "50_40_0_1_UPLOAD_HDFS_FILETYPE_PROCESSING_RULE_START", "50_40_0_5_UPLOAD_HDFS_FILETYPE_PROCESSING_RULE_SUCCESS", "60_10_1_HIVE_TABLE_CREATE_START", "60_10_5_HIVE_TABLE_CREATE_SUCCESS", "60_20_1_HIVE_TABLE_CREATE_TEMP_TABLE_START", "60_20_5_HIVE_TABLE_CREATE_TEMP_TABLE_SUCCESS", "70_10_1_HIVE_TABLE_ADD_PARTITION_START", "70_10_5_HIVE_TABLE_ADD_PARTITION_SUCCESS", "80_10_1_COPY_TO_ORC_START", "80_10_5_COPY_TO_ORC_SUCCESS", "80_20_1_CLEAN_TEMP_TABLE_START" ]
metric_names = ['Backlog', 'Velocity-T1', 'Velocity-T2']

# testStatuses = ["30_10_1_S3_DOWNLOAD_START"]
# testMetricNames = ['Backlog']

for status in statuses:
    for metric_name in metric_names:
        test = hackthonfunction(status, metric_name)
        test.getFile()

# for status in testStatuses:
#     for metric_name in testMetricNames:
#         test = hackthonfunction(status, metric_name)
#         test.getFile()