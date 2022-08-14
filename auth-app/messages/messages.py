import base64
import json
from jwt import (jwk_from_dict)
from jwt.exceptions import JWTDecodeError
import os

public_key = None


def get_keys():
    keys = base64.b64decode(os.environ['OKTA_KEYS'])
    jwks = json.loads(keys)
    for jwk in jwks['keys']:
        public_key = jwk_from_dict(jwk)
    return public_key


def verify(token):
    result = {}
    try:
        result = token.decode(token, public_key, False)
    except JWTDecodeError:
        result = {'statusCode': 403, 'body': 'Forbidden '}
    return result


def get_post_data(body):
    postdata = {}
    for items in body.split('&'):
        values = items.split('=')
        postdata[values[0]] = values[1]
    return postdata


def message(event, context):
    messages = []
    body = get_post_data(event['body'])
    result = verify(body['token'])
    if not bool(result):
        messages.append(body['message'])
        result = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            },
            'body': json.dumps(messages)
        }
    return result


get_keys()
