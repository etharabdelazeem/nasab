import graphene
from models import db, Person


# Define GraphQL types
class PersonType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    gender = graphene.String()
    father_id = graphene.Int()
    mother_id = graphene.Int()
    spouse_id = graphene.Int()


class Query(graphene.ObjectType):
    all_persons = graphene.List(PersonType)
    person_by_id = graphene.Field(PersonType, id=graphene.Int(required=True))

    def resolve_all_persons(self, info):
        return Person.query.all()

    def resolve_person_by_id(self, info, id):
        return Person.query.get(id)


class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        gender = graphene.String()
        father_id = graphene.Int()
        mother_id = graphene.Int()
        spouse_id = graphene.Int()

    person = graphene.Field(PersonType)

    def mutate(self, info, name, gender=None, father_id=None, mother_id=None, spouse_id=None):
        person = Person(name=name, gender=gender, father_id=father_id, mother_id=mother_id, spouse_id=spouse_id)
        db.session.add(person)
        db.session.commit()
        return CreatePerson(person=person)


class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        gender = graphene.String()
        father_id = graphene.Int()
        mother_id = graphene.Int()
        spouse_id = graphene.Int()

    person = graphene.Field(PersonType)

    def mutate(self, info, id, name=None, gender=None, father_id=None, mother_id=None, spouse_id=None):
        person = Person.query.get(id)
        if not person:
            raise Exception("Person not found")

        if name:
            person.name = name
        if gender:
            person.gender = gender
        if father_id is not None:
            person.father_id = father_id
        if mother_id is not None:
            person.mother_id = mother_id
        if spouse_id is not None:
            person.spouse_id = spouse_id

        db.session.commit()
        return UpdatePerson(person=person)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        person = Person.query.get(id)
        if not person:
            raise Exception("Person not found")
        
        db.session.delete(person)
        db.session.commit()
        return DeletePerson(success=True)


class AddSibling(graphene.Mutation):
    class Arguments:
        person_id = graphene.Int(required=True)
        sibling_name = graphene.String(required=True)
        sibling_gender = graphene.String()

    person = graphene.Field(PersonType)

    def mutate(self, info, person_id, sibling_name, sibling_gender=None):
        person = Person.query.get(person_id)
        if not person:
            raise Exception("Person not found")
        
        sibling = Person(name=sibling_name, gender=sibling_gender, father_id=person.father_id, mother_id=person.mother_id)
        db.session.add(sibling)
        db.session.commit()
        return AddSibling(person=sibling)


class AddSpouse(graphene.Mutation):
    class Arguments:
        person_id = graphene.Int(required=True)
        spouse_name = graphene.String(required=True)
        spouse_gender = graphene.String()

    person = graphene.Field(PersonType)

    def mutate(self, info, person_id, spouse_name, spouse_gender=None):
        person = Person.query.get(person_id)
        if not person:
            raise Exception("Person not found")

        spouse = Person(name=spouse_name, gender=spouse_gender)
        db.session.add(spouse)
        db.session.commit()

        # Update the spouse relationship
        person.spouse = spouse
        db.session.commit()

        return AddSpouse(person=spouse)


class AddChild(graphene.Mutation):
    class Arguments:
        parent_id = graphene.Int(required=True)
        child_name = graphene.String(required=True)
        child_gender = graphene.String()

    person = graphene.Field(PersonType)

    def mutate(self, info, parent_id, child_name, child_gender=None):
        parent = Person.query.get(parent_id)
        if not parent:
            raise Exception("Parent not found")

        child = Person(name=child_name, gender=child_gender)
        db.session.add(child)
        db.session.commit()

        # Update the parent-child relationship
        if parent.spouse:
            child.father_id = parent.id if parent.gender == "Male" else parent.spouse.id
            child.mother_id = parent.id if parent.gender == "Female" else parent.spouse.id
        else:
            child.father_id = parent.id
        db.session.commit()

        return AddChild(person=child)


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()
    add_sibling = AddSibling.Field()
    add_spouse = AddSpouse.Field()
    add_child = AddChild.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
