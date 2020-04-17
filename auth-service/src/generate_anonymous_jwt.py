import jwt

jwt_token = jwt.encode({
    "https://hasura.io/jwt/claims": {
        "x-hasura-allowed-roles": ["anonymous"],
        "x-hasura-default-role": "anonymous"
    }
}, key='2235f8adc6b5add923281b0d116c8175', algorithm='HS256')

print(jwt_token)
