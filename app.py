from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from schema import schema
from models import db
from config import Config
from auth import login_manager


app = Flask(__name__)
app.config.from_object(Config)

#Initialize db
db.init_app(app)

#Create the database before the first request
with app.app_context():
    db.create_all()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return "Welcome to Nasab"

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user.password = generate_password_hash(password)

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return redirect("http://localhost:8080/signup")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return redirect("http://localhost:8080/login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

app.add_url_rule(
    '/graphql', 
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.route('/api/relationship/<int:person_id>', methods=['GET'])
@login_required
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
