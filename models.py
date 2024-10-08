from app import db

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)

    # Self-referential relationships for parents and spouse
    father_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    mother_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)

    father = db.relationship('Person', remote_side=[id], foreign_keys=[father_id], backref='children_from_father')
    mother = db.relationship('Person', remote_side=[id], foreign_keys=[mother_id], backref='children_from_mother')

    # Many-to-Many relationship for spouses (if necessary)
    spouse = db.relationship('Person', secondary='spouses', 
                             primaryjoin='Person.id==Spouses.person_id', 
                             secondaryjoin='Person.id==Spouses.spouse_id', 
                             backref='spouses')

# Define the many-to-many relationship for spouses
class Spouses(db.Model):
    __tablename__ = 'spouses'
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    spouse_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
