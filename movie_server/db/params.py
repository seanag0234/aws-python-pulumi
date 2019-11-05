from typing import List


class TableAttribute:
    def __init__(self, name: str, type_: str):
        self.name = name
        self.type_ = type_

    def dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.type_
        }


class GlobalSecondaryIndex:
    def __init__(self, hash_key: str, name: str, read_capacity: int, write_capacity: int, projection_type: str):
        self.hash_key = hash_key
        self.name = name
        self.read_capacity = read_capacity
        self.projection_type = projection_type
        self.write_capacity = write_capacity

    def dict(self):
        return {
            'hash_key': self.hash_key,
            'name': self.name,
            'read_capacity': self.read_capacity,
            'write_capacity': self.write_capacity,
            'projection_type': self.projection_type
        }


class DynamoDBParams:
    def __init__(
            self,
            table_name: str,
            hash_key: str,
            attributes: List[TableAttribute],
            read_capacity: int,
            write_capacity: int,
            global_secondary_indexes: List[GlobalSecondaryIndex],
            should_protect: bool
    ):
        self.table_name = table_name
        self.hash_key = hash_key
        self.attributes = attributes
        self.read_capacity = read_capacity
        self.write_capacity = write_capacity
        self.global_secondary_indexes = global_secondary_indexes
        self.should_protect = should_protect
