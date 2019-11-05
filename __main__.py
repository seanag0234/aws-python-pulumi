from movie_server.db import DB
from movie_server.api.api_gateway import APIGateway
from movie_server.api.params import *

DB.initialize()

test_methods = [
    LambdaMethodParams(
        'AnyMethod',
        'ANY',
        LambdaParams('HelloWorldFunction', 'hello_world.handler', 'HelloWorldFuncPermission'),
        'TestLambdaIntegration'
    )
]

test_resource = APIResourceParams('TestResource', 'test', test_methods)
api_resources = [
    test_resource
]
APIGateway.initialize('TestAPI', api_resources)
