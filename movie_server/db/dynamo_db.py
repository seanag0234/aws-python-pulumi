import pulumi
from pulumi_aws import dynamodb
from pulumi_aws.dynamodb import Table

from movie_server.db.params import DynamoDBParams


class DynamoDB:
    @staticmethod
    def initialize(params: DynamoDBParams) -> Table:
        db_resource_options = pulumi.ResourceOptions(
            protect=params.should_protect,
        )

        table_attributes = [a.dict() for a in params.attributes]

        global_secondary_indexes = [
            index.dict() for index in params.global_secondary_indexes
        ]

        table: Table = dynamodb.Table(
            resource_name=params.table_name,
            opts=db_resource_options,
            hash_key=params.hash_key,
            global_secondary_indexes=global_secondary_indexes,
            read_capacity=params.read_capacity,
            write_capacity=params.write_capacity,
            attributes=table_attributes,
        )

        return table
