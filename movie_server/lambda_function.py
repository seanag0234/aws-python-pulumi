import os

import pulumi
from pulumi_aws import lambda_

from movie_server.iam import lambda_role


class LambdaFunction:
    _lambda_functions_dir = './movie_server/lambda_functions'

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


