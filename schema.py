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

class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

