import os

import pulumi
from pulumi_aws import lambda_

from movie_server.iam import lambda_role


class LambdaFunction:
    @staticmethod
    def create_lambda_function(file_path: str, function_name: str, handler: str) -> lambda_.Function:
        dir_path = file_path
        if not os.path.isdir(dir_path):
            raise Exception(os.getcwd())
        lambda_function = lambda_.Function(
            function_name,
            role=lambda_role.arn,
            runtime='python3.7',
            handler=handler,
            code=pulumi.AssetArchive({
                '.': pulumi.FileArchive(dir_path)
            })
        )
        return lambda_function


