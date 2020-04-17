from flask import request, Response, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from pony.orm import select
from models import User
from app import app
import requests as reqs
import uuid
import json
from datetime import datetime

@app.route('/auth')
def authenticate():
    token = request.headers.get('X-ID-Token')
    CLIENT_ID = '5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com'

    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        google_userid = idinfo['sub']

    except ValueError as e:
        return Response(status=401)
    
    user = select(user for user in User if user.google_userid == google_userid).first()

    if user is None:
        profile = json.loads(reqs.get('https://oauth2.googleapis.com/tokeninfo?id_token=' + token).text)

        new_user = User(
            id=uuid.uuid4(),
            email=profile.get('email'),
            first_name=profile.get('given_name'),
            last_name=profile.get('family_name'),
            created_at=datetime.now(),
            google_userid=google_userid)
        
        return jsonify({
        "X-Hasura-User-Id": new_user.id,
        "X-Hasura-Role": "user"
        })

    return jsonify({
        "X-Hasura-User-Id": user.id,
        "X-Hasura-Role": "user"
    })


@app.route('/')
def hello_world():
    return 'Hello World!'
