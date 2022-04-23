import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Category, Quizzes, Question, Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ('id', 'title', 'category', 'date_created', 'question')

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('title', 'quiz', 'answer')

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('question', 'answer_text', 'id', 'is_right')
    
    
class Query(graphene.ObjectType):
    
    all_quizzes = DjangoListField(QuizzesType)
    all_question = DjangoListField(QuestionType)
    
    get_specific_quiz = graphene.Field(QuizzesType, id=graphene.Int())
    get_specific_question = graphene.Field(QuestionType, id=graphene.Int())
    get_answer_by_question = graphene.List(AnswerType, id=graphene.Int())
    
    def resolve_get_specific_quiz(root, info, id):
        return Quizzes.objects.get(id=id)
    
    def resolve_get_specific_question(root, info, id):
        return Question.objects.get(id=id)
    
    def resolve_get_answer_by_question(root, info, id):
        return Answer.objects.filter(question=id)
    
# mutations

# add category
class CategoryAddMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryAddMutation(category=category)
    
# update category
class CategoryUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryAddMutation(category=category)
    
class CategoryDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    ok = graphene.Boolean()

    
    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return cls(ok=True)
    
    
class Mutation(graphene.ObjectType):
    add_category = CategoryAddMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)