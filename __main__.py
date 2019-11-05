from movie_server.db import DB
from movie_server.api_gateway import APIGateway, APIResource, APIMethodParams, LambdaParams

DB.initialize()

test_methods = [
    APIMethodParams('AnyMethod', 'ANY', LambdaParams('HelloWorldFunction', 'hello_world.handler', 'TestLambdaPermission'),
                    'TestLambdaIntegration')
]

test_resource = APIResource('TestResource', 'test', test_methods)
api_resources = [
    test_resource
]
APIGateway.initialize('TestAPI', api_resources)
