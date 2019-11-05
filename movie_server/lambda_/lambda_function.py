import os

import pulumi
from pulumi_aws import lambda_, apigateway

from movie_server.lambda_.iam import lambda_role


class LambdaFunction:
    _lambda_functions_dir = './movie_server/lambda_/functions'

    @staticmethod
    def create_lambda_function(function_name: str, handler: str) -> lambda_.Function:
        lambda_functions_dir = LambdaFunction._lambda_functions_dir

        if not os.path.isdir(lambda_functions_dir):
            raise Exception(os.getcwd())

        lambda_function = lambda_.Function(
            function_name,
            role=lambda_role.arn,
            runtime='python3.7',
            handler=handler,
            code=pulumi.AssetArchive({
                '.': pulumi.FileArchive(lambda_functions_dir)
            })
        )

        return lambda_function

    @staticmethod
    def create_api_gateway_permission(api: apigateway.RestApi, name: str,
                                      function_name: pulumi.Output[str]):

        # noinspection PyTypeChecker
        source_arn = pulumi.Output.concat(api.execution_arn, '/*')

        LambdaFunction.create_permission(name, 'apigateway.amazonaws.com', function_name, source_arn)

    @staticmethod
    def create_permission(name: str, principal: str, function_name: pulumi.Output[str], source_arn: pulumi.Output[str]):
        lambda_.Permission(
            resource_name=name,
            action="lambda:InvokeFunction",
            function=function_name,
            principal=principal,
            source_arn=source_arn
        )
