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
