import os

import pulumi
import pulumi_aws
from pulumi_aws import apigateway, lambda_

from movie_server.lambda_function import LambdaFunction
from .iam import *


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
        APIGateway.create_resource_with_method(api, 'TestResource')

    @staticmethod
    def create_resource_with_method(api: apigateway.RestApi, resource_name: str) -> None:
        test_resource = apigateway.Resource(
            resource_name=resource_name,
            path_part="test",
            rest_api=api.id,
            parent_id=api.root_resource_id
        )
        test_method = apigateway.Method(
            resource_name='AnyMethod',
            authorization='NONE',
            http_method='ANY',
            rest_api=api.id,
            resource_id=test_resource.id
        )

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
            resource_id=test_resource.id,
            integration_http_method='POST',
            http_method=test_method.http_method,
            type="AWS_PROXY",
            uri=hello_world_fn.invoke_arn
        )

