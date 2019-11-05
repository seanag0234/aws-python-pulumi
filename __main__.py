from movie_server.api.api_gateway import APIGateway
from movie_server.api.params import *
from movie_server.db.dynamo_db import DynamoDB
from movie_server.db.movie_server_db import MovieServerDB

db_params = MovieServerDB.db_params()

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
