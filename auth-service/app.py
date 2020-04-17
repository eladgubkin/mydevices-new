from flask import Flask
from pony.flask import Pony
from models import db, User
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
from flask_graphql import GraphQLView

app = Flask(__name__)
Pony(app)


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
        }, key='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', algorithm='HS256')

        return LoginWithGoogle(jwt_token=jwt_token.decode('ascii'))


class Query(graphene.ObjectType):
    name = graphene.String()


class Mutations(graphene.ObjectType):
    login_with_google = LoginWithGoogle.Field()


schema = graphene.Schema(
    mutation=Mutations,
    query=Query
)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                                                           schema=schema, graphiql=True))


if __name__ == '__main__':
    db.bind(provider='postgres', user='postgres', port=5432,
            password='postgrespassword', host='postgres', database='postgres')
    db.generate_mapping(create_tables=False)
    app.run(host="0.0.0.0", port=5000, debug=True)
