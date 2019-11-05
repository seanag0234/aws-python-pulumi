from poc.db.params import TableAttribute, GlobalSecondaryIndex, DynamoDBParams


class TestDB:
    @staticmethod
    def db_params():
        item_id = 'ItemID'
        user_email = 'UserEmail'
        table_attributes = [
            TableAttribute(item_id, 'S'),
            TableAttribute(user_email, 'S'),
        ]
        global_secondary_indexes = [
            GlobalSecondaryIndex(
                hash_key=user_email,
                name='UserEmailIndex',
                read_capacity=10,
                write_capacity=10,
                projection_type='ALL'
            )
        ]
        db_params = DynamoDBParams(
            table_name='TestTable',
            hash_key=item_id,
            attributes=table_attributes,
            read_capacity=10,
            write_capacity=10,
            global_secondary_indexes=global_secondary_indexes,
            should_protect=False
        )
        return db_params
