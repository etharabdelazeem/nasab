import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Hello, Nasab!"

schema = graphene.Schema(query=Query)
