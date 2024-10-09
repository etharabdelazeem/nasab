from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from schema import schema
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#Initialize db
db.init_app(app)

#Create the database before the first request
with app.app_context():
    db.create_all()
    print("Tables created!")

@app.route('/')
def index():
    return "Welcome to Nasab"


app.add_url_rule(
    '/graphql', 
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
