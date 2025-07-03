import json
import boto3
import os

TABLE_NAME = os.environ.get("STORAGE_USERTABLE_NAME", "userTabel-dev")
EMAIL_INDEX_NAME = "EmailIndex"

dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    print("Received event:")
    print(event)

    try:
        email = event.get("email")

        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'email' in request"})
            }

        response = table.query(
            IndexName=EMAIL_INDEX_NAME,
            KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
        )

        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": '*',
                "Access-Control-Allow-Origin": '*',
                "Access-Control-Allow-Methods": 'OPTIONS,POST,GET'
            },
            "body": json.dumps(items[0])  # return the first match
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
