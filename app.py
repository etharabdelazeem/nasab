from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from schema import schema
from models import db, User, Person
from config import Config
from auth import login_manager

migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)

#Initialize db
db.init_app(app)
migrate.init_app(app, db)

#Create the database before the first request
with app.app_context():
    db.create_all()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to 'login' route
login_manager.login_message = 'You need to log in to access this page.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Create the user first
        new_user = User(username=username, password=generate_password_hash(password))
        
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return render_template('login.html')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form.get('gender')  # Optional field
        father_id = request.form.get('father_id')  # Optional, can be empty
        mother_id = request.form.get('mother_id')  # Optional, can be empty
        spouse_id = request.form.get('spouse_id')  # Optional, can be empty

        # Create new family member
        new_member = Person(
            name=name,
            gender=gender,
            father_id=father_id if father_id else None,
            mother_id=mother_id if mother_id else None,
            spouse_id=spouse_id if spouse_id else None
        )

        db.session.add(new_member)
        db.session.commit()
        flash(f'{name} has been added as a new family member!', 'success')
        return render_template('dashboard.html', name=current_user.username)  # Redirect to the dashboard

    # For GET requests, retrieve existing family members to populate dropdowns
    family_members = Person.query.all()
    return render_template('add_member.html', family_members=family_members)

@app.route('/family', methods=['GET'])
@login_required
def family():
    family_members = Person.query.all()  # Fetch all family members
    return render_template('family.html', family_members=family_members)

app.add_url_rule(
    '/graphql', 
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

@app.route('/search_family', methods=['GET', 'POST'])
@login_required
def search_family():
    if request.method == 'POST':
        query = request.form['query']
        results = Person.query.filter(Person.name.ilike(f'%{query}%')).all()
        return render_template('search_results.html', results=results)

    return render_template('search_family.html')

@app.route('/search_suggestions', methods=['GET'])
@login_required
def search_suggestions():
    query = request.args.get('query', '')
    suggestions = Person.query.filter(Person.name.ilike(f'%{query}%')).limit(5).all()
    return jsonify([person.name for person in suggestions])


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


@app.errorhandler(401)
def unauthorized_error(e):
    flash('Unauthorized access. Please log in first.', 'warning')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    flash('The page you are looking for does not exist.', 'danger')
    return redirect(url_for('dashboard'))


@app.errorhandler(500)
def internal_server_error(e):
    flash('An unexpected error occurred. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
