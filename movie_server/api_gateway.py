import pulumi
from pulumi_aws import apigateway, lambda_

from movie_server.lambda_function import LambdaFunction


class APIGateway:
    @staticmethod
    def initialize(dependencies=None):
        if dependencies is None:
            dependencies = []
        resource_options = pulumi.ResourceOptions(
            depends_on=dependencies
        )
        api = apigateway.RestApi(
            # policy=api_gateway_role_policy.policy,
            resource_name="TestAPI",
            opts=resource_options,
        )
        resource = APIGateway.create_resource(api, 'TestResource', 'test')
        method = APIGateway.create_method(api, resource, 'AnyMethod', 'ANY')

        hello_world_fn = LambdaFunction.create_lambda_function('HelloWorldFunction', 'hello_world.handler')

        LambdaFunction.create_api_gateway_permission(api, 'TestLambdaPermission', hello_world_fn.name)

        APIGateway.create_lambda_integration('TestLambdaIntegration', api, hello_world_fn, method, resource)

    @staticmethod
    def create_lambda_integration(name: str, api: apigateway.RestApi, lambda_function: lambda_.Function,
                                  method: apigateway.Method, resource: apigateway.Resource):
        apigateway.Integration(
            resource_name=name,
            rest_api=api.id,
            resource_id=resource.id,
            integration_http_method='POST',
            http_method=method.http_method,
            type="AWS_PROXY",
            uri=lambda_function.invoke_arn
        )

    @staticmethod
    def create_resource(api: apigateway.RestApi, name: str, path_part: str) -> apigateway.Resource:
        resource = apigateway.Resource(
            resource_name=name,
            path_part=path_part,
            rest_api=api.id,
            parent_id=api.root_resource_id
        )
        return resource

    @staticmethod
    def create_method(api: apigateway.RestApi, resource: apigateway.Resource, name: str, http_method: str,
                      authorization='NONE') -> apigateway.Method:
        method = apigateway.Method(
            resource_name=name,
            authorization=authorization,
            http_method=http_method,
            rest_api=api.id,
            resource_id=resource.id
        )
        return method
