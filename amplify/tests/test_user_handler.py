import boto3
import moto 
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname("./amplify/backend/functions/user_handler/src")))
import index as handler



# @mock_dynamodb
# def test_user_handler():
#     dynamo_db = boto3.resource('dynamodb', region_name='us-west-1')
#     table = dynamo_db.create_table(
#         TableName='UserTable',
#         KeySchema=[
#             {
#                 'AttributeName': 'user_id',
#                 'KeyType': 'HASH'
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'user_id',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'email',
#                 'AttributeType': 'S'
#             }
#         ],
#         GlobalSecondaryIndexes=[
#             {
#                 'IndexName': 'email-index',
#                 'KeySchema': [
#                     {
#                         'AttributeName': 'email',
#                         'KeyType': 'HASH'
#                     }
#                 ],
#                 'Projection': {
#                     'ProjectionType': 'ALL'
#                 },
#                 'ProvisionedThroughput': {
#                     'ReadCapacityUnits': 1,
#                     'WriteCapacityUnits': 1
#                 }
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 1,
#             'WriteCapacityUnits': 1
#         }
#     )
#     table.meta.client.get_waiter('table_exists').wait(TableName='UserTable')