import boto3
import logging


def create_batch_prediction():
    logger.debug("create a data source for the s3 file")
    data_source = machine_learning.create_data_source_from_s3(
        DataSourceId='id-dataSourceId',
        DataSourceName='AutoDataSource',
        DataSpec={
            'DataLocationS3': 's3://panto.eab.archive.local/hackathon/testdata.csv',
            'DataRearrangement': 'string',
            'DataSchema': 'DataSchema',
            'DataSchemaLocationS3': 's3://panto.eab.archive.local/hackathon/'
        },
        ComputeStatistics=False
    )

    batch_prediction = machine_learning.create_batch_prediction(
        BatchPredictionId='id-batchPredictionId',
        BatchPredictionName='AutoBatchPrediction',
        MLModelId='ml-axihsyIeR1J',
        BatchPredictionDataSourceId='ds-jbCZsfecgKK',
        OutputUri='s3://panto.eab.archive.local/hackathon/mlresult'
    )






logger = logging.getLogger(__name__)


logger.debug("init db connection")
logger.debug("init s3")
s3 = boto3.client('s3')
logger.debug("init machinelearning")
machine_learning = boto3.client('machinelearning')
logger.debug("Initialization completed")