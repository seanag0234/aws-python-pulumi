import pulumi
from pulumi_aws import apigateway, lambda_
from pulumi_aws.apigateway import RestApi

from poc.api.api_gateway_deployer import APIGatewayDeployer
from poc.lambda_.lambda_function import LambdaFunction
from .params import *


class APIGatewayInitializer:
    @staticmethod
    def initialize(
            api_name: str,
            resources: List[APIResourceParams],
            dependencies: List[pulumi.Resource] = None
    ) -> APIGatewayDeployer:
        if dependencies is None:
            dependencies = []

        api: RestApi = APIGatewayInitializer.create_api(api_name, dependencies)
        integrations = APIGatewayInitializer.create_resources(api, resources)

        return APIGatewayDeployer(api, integrations)

    @staticmethod
    def create_resources(api: apigateway.RestApi, resources: List[APIResourceParams]) -> List[apigateway.Integration]:
        integrations: List[apigateway.Integration] = []
        for resource in resources:
            created_resource = APIGatewayInitializer.create_resource(api, resource.name, resource.path_part)
            for method in resource.methods:
                created_method = APIGatewayInitializer.create_method(api, created_resource, method.name,
                                                                     method.http_method)
                lambda_params = method.lambda_params
                lambda_function = LambdaFunction.create_lambda_function(lambda_params.name, lambda_params.handler)
                LambdaFunction.create_api_gateway_permission(api, lambda_params.permission_name, lambda_function.name)
                new_integration = APIGatewayInitializer.create_lambda_integration(
                    method.api_integration_name,
                    api,
                    lambda_function,
                    created_method,
                    created_resource
                )
                integrations.append(new_integration)

        return integrations

    @staticmethod
    def create_api(api_name: str, dependencies: List[pulumi.Resource]) -> apigateway.RestApi:
        resource_options = pulumi.ResourceOptions(
            depends_on=dependencies
        )
        api = apigateway.RestApi(
            resource_name=api_name,
            opts=resource_options,
        )
        return api

    @staticmethod
    def create_lambda_integration(
            name: str,
            api: apigateway.RestApi,
            lambda_function: lambda_.Function,
            method: apigateway.Method,
            resource: apigateway.Resource
    ) -> apigateway.Integration:
        integration = apigateway.Integration(
            resource_name=name,
            rest_api=api.id,
            resource_id=resource.id,
            integration_http_method='POST',
            http_method=method.http_method,
            type="AWS_PROXY",
            uri=lambda_function.invoke_arn
        )
        return integration

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
    def create_method(
            api: apigateway.RestApi,
            resource: apigateway.Resource,
            name: str,
            http_method: str,
            authorization='NONE'
    ) -> apigateway.Method:
        method = apigateway.Method(
            resource_name=name,
            authorization=authorization,
            http_method=http_method,
            rest_api=api.id,
            resource_id=resource.id
        )
        return method
