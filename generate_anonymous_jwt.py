import jwt

jwt_token = jwt.encode({
    "https://hasura.io/jwt/claims": {
        "x-hasura-allowed-roles": ["anonymous"],
        "x-hasura-default-role": "anonymous"
    }
}, key='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', algorithm='HS256')

print(jwt_token)
