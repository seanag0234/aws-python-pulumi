from poc.api.api_gateway import APIGateway
from poc.api.params import *
from poc.db.dynamo_db import DynamoDB
from poc.db.test_db import TestDB

db_params = TestDB.db_params()

DynamoDB.initialize(db_params)

test_methods = [
    LambdaMethodParams(
        'AnyMethod',
        'GET',
        LambdaParams('HelloWorldFunction', 'hello_world.handler', 'HelloWorldFuncPermission'),
        'TestLambdaIntegration'
    )
]

test_resource = APIResourceParams('TestResource', 'test', test_methods)
api_resources = [
    test_resource
]
APIGateway.initialize('TestAPI', api_resources)
