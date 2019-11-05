import os

import pulumi
import pulumi_aws
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

        source_arn = pulumi.Output.concat(api.execution_arn, '/*')

        lambda_.Permission(
            resource_name="TestLambdaPermission",
            statement_id='AllowExecutionFromAPIGateway',
            action="lambda:InvokeFunction",
            function=hello_world_fn.name,
            principal="apigateway.amazonaws.com",
            source_arn=source_arn
        )
        apigateway.Integration(
            resource_name="TestLambdaIntegration",
            rest_api=api.id,
            resource_id=resource.id,
            integration_http_method='POST',
            http_method=method.http_method,
            type="AWS_PROXY",
            uri=hello_world_fn.invoke_arn
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
