# main schema
import graphene
from books.schema import Query as BooksQuery
from quiz.schema import Query as QuizQuery
from quiz.schema import Mutation as QuizMutation

class Query(QuizQuery, BooksQuery):
    pass

class Mutation(QuizMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)