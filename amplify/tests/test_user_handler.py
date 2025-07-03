import boto3
from moto import mock_dynamodb
import pytest
import uuid
import sys
import os
import json

# Import the handler function
sys.path.append(os.path.abspath("./amplify/backend/functions/user_handler/src"))
import index as handler

TABLE_NAME = "UserTabel-dev"  # Use the same table name as in the handler
EMAIL_INDEX_NAME = "email-index"

@mock_dynamodb
def test_post_and_get_user():
    # Set env variable
    os.environ["STORAGE_USERTABLE_NAME"] = TABLE_NAME

    # Create mock table
    dynamo_db = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamo_db.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {'AttributeName': 'userId', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'userId', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': EMAIL_INDEX_NAME,
                'KeySchema': [
                    {'AttributeName': 'email', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)

    # Test 1: POST a user
    test_email = "test@example.com"
    post_response = handler.handler({"email": test_email}, {})
    assert post_response["statusCode"] == 200
    user_id = json.loads(post_response["body"])["user_id"]

    # Test 2: GET the same user
    # Override handler to use query logic (you may have this in another function)
    # Simulating the GET handler
    from boto3.dynamodb.conditions import Key

    response = table.query(
        IndexName=EMAIL_INDEX_NAME,
        KeyConditionExpression=Key("email").eq(test_email)
    )
    items = response.get("Items", [])

    assert len(items) == 1
    assert items[0]["userId"] == user_id
    assert items[0]["email"] == test_email
