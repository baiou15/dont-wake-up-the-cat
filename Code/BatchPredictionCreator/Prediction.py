import boto3
import logging
import csv
import pandas as pd
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


# def lambda_handler(event, context):
#     logger.debug("init s3")
#     s3 = boto3.resource('s3')
#     ec2 = boto3.client('ec2', region_name='us-east-1')
#
#     bucket = s3.Bucket(u'panto.eab.archive.dev')
#     obj = bucket.Object(key=u'hackathon/prediction.csv')
#     response = obj.get()
#     lines = response[u'Body'].read().split()
#
#     for row in csv.DictReader(lines):
#         if abs(row[1]) > 0.7:
#             logger.info('Cluster Import seems getting stuck, will reboot the instance...')
#             try:
#                 ec2.reboot_instances(InstanceIds=[''], DryRun=True)
#             except ClientError as e:
#                 if 'DryRunOperation' not in str(e):
#                     print("You don't have permission to reboot instances.")
#                     raise
#
#             try:
#                 response = ec2.reboot_instances(InstanceIds=[''], DryRun=False)
#                 print("Reboot succeeded!", response)
#             except ClientError as e:
#                 print('Error', e)


# logger.debug("init s3")
# s3 = boto3.resource('s3')
# ec2 = boto3.client('ec2', region_name='us-east-1')
#
# bucket = s3.Bucket(u'panto.eab.archive.dev')
# obj = bucket.Object(key=u'hackathon/prediction.csv')
# response = obj.get()
# lines = response[u'Body'].read().split()
#
# for row in csv.DictReader(lines):
#     if abs(row[1]) > 0.7:
#         logger.info('Cluster Import seems getting stuck, will reboot the instance...')
#         try:
#             ec2.reboot_instances(InstanceIds=[''], DryRun=True)
#         except ClientError as e:
#             if 'DryRunOperation' not in str(e):
#                 print("You don't have permission to reboot instances.")
#                 raise
#
#         try:
#             response = ec2.reboot_instances(InstanceIds=[''], DryRun=False)
#             print("Reboot succeeded!", response)
#         except ClientError as e:
#             print('Error', e)


grid_sizes = pd.read_csv('../../prediction.csv')

print(grid_sizes)