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
    docid = event['queryStringParameters']['documentId']
    vid = event['queryStringParameters']['versionId']

    try:
        ddbclient = get_ddb_connection()
        response = ddbclient.get_item(
            TableName=os.environ['DDBTableName'],
            Key={
                'documentId':{'N': docid},
                'versionId':{'S': vid}
            },
            AttributesToGet=[
                'location',
            ],
        )

        logging.info(response)

        if 'Item' in response:
            low_level_data = dict(response['Item'])

            boto3.resource('dynamodb')
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            python_data = {k: deserializer.deserialize(v) for k,v in low_level_data.items()}
            logging.info(python_data)

            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                'body': json.dumps({
                    'message': python_data,
                }),
            }
        
        else:
            return {
                'statusCode': '404',
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                'body': json.dumps({
                    'message': 'Item not found',
                }),
            }

    except ddbclient.exceptions.ResourceNotFoundException as e:
        logging.error('Cannot do operations on a non-existent table')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e