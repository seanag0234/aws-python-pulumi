from typing import List, Dict

import pulumi
from pulumi_aws import apigateway, lambda_

from movie_server.lambda_function import LambdaFunction


class LambdaParams:
    def __init__(self, name: str, handler: str, permission_name: str):
        self.name = name
        self.handler = handler
        self.permission_name = permission_name


class APIMethodParams:
    def __init__(self, name: str, http_method: str, lambda_params: LambdaParams, api_integration_name: str):
        self.name = name
        self.http_method = http_method
        self.lambda_params = lambda_params
        self.api_integration_name = api_integration_name


class APIResource:
    def __init__(self, name: str, path_part: str, methods: List[APIMethodParams]):
        self.path_part = path_part
        self.name = name
        self.methods = methods


class APIGateway:
    @staticmethod
    def initialize(api_name: str, resources: List[APIResource], dependencies: List[pulumi.Resource] = None):
        if dependencies is None:
            dependencies = []

        for resource in resources:
            api = APIGateway.create_api(api_name, dependencies)
            created_resource = APIGateway.create_resource(api, resource.name, resource.path_part)
            for method in resource.methods:
                created_method = APIGateway.create_method(api, created_resource, method.name, method.http_method)
                lambda_params = method.lambda_params
                lambda_function = LambdaFunction.create_lambda_function(lambda_params.name, lambda_params.handler)
                LambdaFunction.create_api_gateway_permission(api, lambda_params.permission_name, lambda_function.name)
                APIGateway.create_lambda_integration(
                    method.api_integration_name,
                    api,
                    lambda_function,
                    created_method,
                    created_resource
                )

    @staticmethod
    def create_api(api_name, dependencies):
        resource_options = pulumi.ResourceOptions(
            depends_on=dependencies
        )
        api = apigateway.RestApi(
            resource_name=api_name,
            opts=resource_options,
        )
        return api

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
