from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'persons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))  # Optional field for gender
    father_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)
    mother_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)
    spouse_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)

    # Relationships
    father = db.relationship('Person', remote_side=[id], backref='children_father', 
                             foreign_keys=[father_id])
    mother = db.relationship('Person', remote_side=[id], backref='children_mother', 
                             foreign_keys=[mother_id])
    spouse = db.relationship('Person', remote_side=[id], backref='spouses', 
                             foreign_keys=[spouse_id])

    def __repr__(self):
        return f'<Person {self.name}>'

