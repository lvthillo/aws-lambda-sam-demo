# aws-lambda-sam-demo
Demo project which uses SAM and AWS lambda to test lambdas locally.
A company has a lot of documents. The documents have a unique ID. It's also possible to have multiple versions of one document. The employees of the company have issues to find out where a certain version of a certain document is stored. To solve this the company has developed a solution to make it easy to query the storage location of a document.

![SAM(2)](https://user-images.githubusercontent.com/14105387/76995481-36729300-6950-11ea-81a8-a33d8a91b6a0.png)

# local setup

Deploy DynamoDB in Docker
```
$ docker network create sam-demo
$ docker run --network sam-demo --name dynamodb -d -p 8000:8000 amazon/dynamodb-local
$ aws dynamodb create-table --table-name documentTable --attribute-definitions AttributeName=documentId,AttributeType=N AttributeName=versionId,AttributeType=S --key-schema AttributeName=documentId,KeyType=HASH AttributeName=versionId,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:8000
```

Build SAM application
```
$ sam build --use-container
```

Invoke load data function to load data in DynamoDB and verify
```
$ sam local invoke LoadDataFunction --parameter-overrides ParameterKey=Environment,ParameterValue=local ParameterKey=DDBTableName,ParameterValue=documentTable --docker-network sam-demo
$ aws dynamodb scan --table-name documentTable --endpoint-url http://localhost:8000
```

Start local API Gateway
```
$ sam local start-api --parameter-overrides ParameterKey=Environment,ParameterValue=local ParameterKey=DDBTableName,ParameterValue=documentTable --docker-network sam-demo
```

Test with curl
```
$ curl "http://127.0.0.1:3000/document?documentId=1044&versionId=v_1"
{"message": {"location": "s3://bucket-a/8853806831.doc"}}
```

Open the static web application



# AWS setup
```
$ sam build --use-container
$ sam deploy --template-file .aws-sam/build/template.yaml --s3-bucket xxcx-bucket  --parameter-overrides ParameterKey=Environment,ParameterValue=aws ParameterKey=DDBTableName,ParameterValue=documentTable --stack-name aws-lambda-sam-demo --capabilities CAPABILITY_NAMED_IAM
```
