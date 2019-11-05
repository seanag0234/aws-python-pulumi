import pulumi
from pulumi_aws import s3, apigateway, dynamodb, cognito


def init_db(table_name='TestDB'):
    db_resource_options = pulumi.ResourceOptions(
        protect=False,
    )

    user_email = 'UserEmail'
    item_id = 'ItemId'
    table_attributes = [
        {'name': item_id, 'type': 'S'},
        {'name': user_email, 'type': 'S'},
    ]

    read_capacity = 10
    write_capacity = 10

    global_secondary_indexes = [
        {
            'hash_key': user_email,
            'name': "UserEmailSecondaryIndex",
            'read_capacity': read_capacity,
            'write_capacity': write_capacity,
            'projectionType': 'ALL'
        }
    ]

    dynamodb.Table(
        resource_name=table_name,
        opts=db_resource_options,
        hash_key=item_id,
        global_secondary_indexes=global_secondary_indexes,
        read_capacity=read_capacity,
        write_capacity=write_capacity,
        attributes=table_attributes,
    )
