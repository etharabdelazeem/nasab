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

@app.route('/')
def index():
    return "Welcome to Nasab"


app.add_url_rule(
    '/graphql', 
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.route('/api/relationship/<int:person_id>', methods=['GET'])
def get_relationship(person_id):
    user = get_current_user()  # Fetch the logged-in user
    person = Person.query.get_or_404(person_id)  # Get the person by ID

    # Use the RelationshipMapper to determine the relationship
    relationship_mapper = RelationshipMapper(user)
    relationship = relationship_mapper.determine_relationship(person)

    return jsonify({
        'relationship': relationship
    })

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
