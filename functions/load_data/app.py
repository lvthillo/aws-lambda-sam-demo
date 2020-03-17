import os
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_ddb_connection():
    ENV = os.environ['Environment']
    ddbclient=''
    if ENV == 'local':
        ddbclient = boto3.client('dynamodb', endpoint_url='http://dynamodb:8000/')
    else:
        ddbclient = boto3.client('dynamodb')
    return ddbclient

def lambda_handler(event, context):
    ddbclient = get_ddb_connection()
    try:
        response = ddbclient.batch_write_item(
        RequestItems={
            os.environ['DDBTableName']: [
                {
                    'PutRequest': {
                        'Item': {
                            'documentId': {'N': '1043'},
                            'versionId': {'S': 'v_1'},
                            'location': {'S': 's3://bucket-a/6591636740.doc'}
                        }
                    }
                },
                {
                    'PutRequest': {
                        'Item': {
                            'documentId': {'N': '1043'},
                            'versionId': {'S': 'v_2'},
                            'location': {'S': 's3://bucket-b/2816684052.doc'}
                        }
                    }
                },
                {
                    'PutRequest': {
                        'Item': {
                            'documentId': {'N': '1044'},
                            'versionId': {'S': 'v_1'},
                            'location': {'S': 's3://bucket-a/8853806831.doc'}
                        }
                    }
                },
                {
                    'PutRequest': {
                        'Item': {
                            'documentId': {'N': '1045'},
                            'versionId': {'S': 'v_1'},
                            'location': {'S': 's3://bucket-a/7100394559.doc'}
                        }
                    }
                },
                {
                    'PutRequest': {
                        'Item': {
                            'documentId': {'N': '1045'},
                            'versionId': {'S': 'v_2'},
                            'location': {'S': 's3://bucket-c/2897476413.doc'}
                        }
                    }
                },
            ]}
        )

        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps({
                'message': 'Filled DynamoDB',
            }),
        }

    except ddbclient.exceptions.ResourceNotFoundException as e:
        logging.error('Cannot do operations on a non-existent table')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e

