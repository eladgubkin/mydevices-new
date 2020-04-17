import graphene
from mutations import Mutations


class Query(graphene.ObjectType):
    name = graphene.String()


schema = graphene.Schema(
    mutation=Mutations,
    query=Query
)
