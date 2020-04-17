from models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from pony.orm import select
from graphql import GraphQLError
import uuid
import json
import requests as reqs
from datetime import datetime
import graphene
import jwt


class LoginWithGoogle(graphene.Mutation):
    class Arguments:
        google_token = graphene.String(required=True)

    jwt_token = graphene.String()

    def mutate(root, info, google_token):
        CLIENT_ID = '5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com'

        try:
            idinfo = id_token.verify_oauth2_token(
                google_token, requests.Request(), CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            google_userid = idinfo['sub']

        except ValueError:
            raise GraphQLError('Invalid Token')

        user = select(user for user in User if user.google_userid ==
                      google_userid).first()

        if user is None:
            profile = json.loads(reqs.get(
                'https://oauth2.googleapis.com/tokeninfo?id_token=' + google_token).text)

            user = User(
                id=uuid.uuid4(),
                email=profile.get('email'),
                first_name=profile.get('given_name'),
                last_name=profile.get('family_name'),
                created_at=datetime.now(),
                google_userid=google_userid)

        jwt_token = jwt.encode({
            "https://hasura.io/jwt/claims": {
                "x-hasura-allowed-roles": ["user"],
                "x-hasura-default-role": "user",
                "x-hasura-user-id": str(user.id),
            }
        }, key='2235f8adc6b5add923281b0d116c8175', algorithm='HS256')

        return LoginWithGoogle(jwt_token=jwt_token.decode('ascii'))


class Mutations(graphene.ObjectType):
    login_with_google = LoginWithGoogle.Field()
