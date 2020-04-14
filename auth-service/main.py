from flask import Flask, request, Response, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from pony.flask import Pony
from pony.orm import select
from models import db, User

app = Flask(__name__)
Pony(app)


@app.route('/auth')
def hello_world():
    token = request.headers.get('X-ID-Token')
    CLIENT_ID = '5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com'

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        google_userid = idinfo['sub']
    except ValueError as e:
        return Response(status=401)

    user = select(user for user in User if user.google_userid ==
                  google_userid).first()

    if user is None:
        return Response(status=401)

    return jsonify({
        "X-Hasura-User-Id": user.id,
        "X-Hasura-Role": "user"
    })


if __name__ == '__main__':
    db.bind(provider='postgres', user='postgres', port=5432,
            password='postgrespassword', host='postgres', database='postgres')
    db.generate_mapping(create_tables=False)
    app.run(host="0.0.0.0", port=5000, debug=True)
