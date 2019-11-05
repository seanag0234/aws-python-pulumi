import json


def handler(event, context):
    body = {
        'response': 'Hi there!'
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }
