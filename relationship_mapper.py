# relationship_mapper.py

class RelationshipMapper:
    def __init__(self, user):
        """
        Initializes the RelationshipMapper for a given user.
        """
        self.user = user
        self.user_family = self._fetch_user_family()

    def _fetch_user_family(self):
        """
        Fetches the user's family tree from the database.
        """
        return {
            'father': self.user.father,
            'mother': self.user.mother,
            'spouse': self.user.spouse,
            'siblings': Person.query.filter_by(father_id=self.user.father_id, mother_id=self.user.mother_id).all(),
            'children': Person.query.filter_by(father_id=self.user.id).all() + Person.query.filter_by(mother_id=self.user.id).all(),
            'grandparents': self._fetch_grandparents(),
            'aunts_uncles': self._fetch_aunts_uncles(),
            'cousins': self._fetch_cousins(),
            'step_parents': self._fetch_step_parents(),
            'half_siblings': self._fetch_half_siblings(),
            'in_laws': self._fetch_in_laws(),
        }

    def _fetch_grandparents(self):
        """
        Fetches grandparents based on user's parents.
        """
        grandparents = []
        if self.user.father:
            if self.user.father.father_id:
                grandparents.append(Person.query.get(self.user.father.father_id))
            if self.user.father.mother_id:
                grandparents.append(Person.query.get(self.user.father.mother_id))
        if self.user.mother:
            if self.user.mother.father_id:
                grandparents.append(Person.query.get(self.user.mother.father_id))
            if self.user.mother.mother_id:
                grandparents.append(Person.query.get(self.user.mother.mother_id))
        return grandparents

    def _fetch_aunts_uncles(self):
        """
        Fetches aunts and uncles based on user's grandparents.
        """
        aunts_uncles = []
        for grandparent in self._fetch_grandparents():
            aunts_uncles += Person.query.filter(
                db.and_(Person.father_id == grandparent.id, Person.id != self.user.father_id)
            ).all()  # Exclude user's parents from aunts/uncles
        return aunts_uncles

    def _fetch_cousins(self):
        """
        Fetches cousins based on user's aunts and uncles.
        """
        cousins = []
        for aunt_uncle in self._fetch_aunts_uncles():
            cousins += Person.query.filter_by(father_id=aunt_uncle.id).all()
        return cousins

    def _fetch_step_parents(self):
        """
        Fetches step-parents based on remarried parents.
        """
        step_parents = []
        if self.user.mother and self.user.mother.spouse_id and self.user.mother.spouse_id != self.user.father_id:
            step_parents.append(Person.query.get(self.user.mother.spouse_id))
        if self.user.father and self.user.father.spouse_id and self.user.father.spouse_id != self.user.mother_id:
            step_parents.append(Person.query.get(self.user.father.spouse_id))
        return step_parents

    def _fetch_half_siblings(self):
        """
        Fetches half-siblings (siblings with one shared parent).
        """
        half_siblings = []
        if self.user.mother_id:
            half_siblings += Person.query.filter_by(mother_id=self.user.mother_id).filter(Person.father_id != self.user.father_id).all()
        if self.user.father_id:
            half_siblings += Person.query.filter_by(father_id=self.user.father_id).filter(Person.mother_id != self.user.mother_id).all()
        return half_siblings

    def _fetch_in_laws(self):
        """
        Fetches in-laws based on spouse's family.
        """
        in_laws = []
        if self.user.spouse:
            in_laws += Person.query.filter_by(father_id=self.user.spouse.father_id).all()
            in_laws += Person.query.filter_by(mother_id=self.user.spouse.mother_id).all()
        return in_laws

    def determine_relationship(self, person):
        """
        Determines the relationship between the user and a given person.
        """
        if person == self.user:
            return "Yourself"

        # Check for direct relationships
        if person == self.user_family['father']:
            return "Your Father"
        if person == self.user_family['mother']:
            return "Your Mother"
        if person == self.user_family['spouse']:
            return "Your Spouse"

        # Check for siblings
        if person in self.user_family['siblings']:
            return "Your Sibling"

        # Check for children
        if person in self.user_family['children']:
            return "Your Child"

        # Check for grandparents
        if person in self.user_family['grandparents']:
            return "Your Grandparent"

        # Check for aunts/uncles
        if person in self.user_family['aunts_uncles']:
            return "Your Aunt/Uncle"

        # Check for cousins
        if person in self.user_family['cousins']:
            return "Your Cousin"

        # Check for step-parents
        if person in self.user_family['step_parents']:
            return "Your Step-parent"

        # Check for half-siblings
        if person in self.user_family['half_siblings']:
            return "Your Half-sibling"

        # Check for in-laws
        if person in self.user_family['in_laws']:
            return "Your In-law"

        # Additional relationship logic can go here (e.g., second cousins, great aunts/uncles)

        return "No Direct Relationship Found"
