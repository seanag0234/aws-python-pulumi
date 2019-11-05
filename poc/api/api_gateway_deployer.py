from typing import List

import pulumi
from pulumi_aws import apigateway


class APIGatewayDeployer:
    def __init__(self, api: apigateway.RestApi, api_integrations: List[apigateway.Integration]):
        self.api = api
        self.api_integrations = api_integrations

    def deploy(self, deployment_name: str, stage_name: str) -> apigateway.Deployment:
        resource_options = pulumi.ResourceOptions(
            depends_on=self.api_integrations
        )
        return apigateway.Deployment(
            resource_name=deployment_name,
            rest_api=self.api.id,
            stage_name=stage_name,
            opts=resource_options
        )
