from typing import List


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


class APIResourceParams:
    def __init__(self, name: str, path_part: str, methods: List[APIMethodParams]):
        self.path_part = path_part
        self.name = name
        self.methods = methods
