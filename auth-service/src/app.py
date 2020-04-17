from flask import Flask
from flask_graphql import GraphQLView
from pony.flask import Pony
from models import db
from schema import schema


app = Flask(__name__)
Pony(app)

app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    db.bind(provider='postgres', user='postgres',
            port=5432, password='postgrespassword',
            host='postgres', database='postgres')

    db.generate_mapping(create_tables=False)
    app.run(host="0.0.0.0", port=5000, debug=True)
