from rest_framework import viewsets
from rest_framework.response import Response
from .models import Question, Choice
from .serializers import QuestionSerializer, QuestionCategorySerializer
from django.db.models import Q
from random import choice

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer


    def get_queryset(self):

        quiz_len = 15
        #limit = self.request.query_params.get("limit", 15)
        cat_dict = {}
        for key, val in self.request.query_params.items():
            print(key, val)
            true_categories = QuestionCategorySerializer.Meta.fields[3:]
            if key in true_categories:
                if val == 'true':
                    val = True
                cat_dict[str("categories__" + key)] = val

        print(cat_dict)

        query = Q()
        for (key,val) in cat_dict.items():
            query |= Q(**{key : val})

        if self.request.query_params.get("time_period") != "*":
            query &= Q(categories__time_period = self.request.query_params.get("time_period"))

        #query &= Q(categories__difficulty = self.request.query_params.get("difficulty")) ## DIFFICULTY

        available = Question.objects.filter(query)
        pkList = list(available.values_list('id', flat=True))
        print(type(pkList))
        quiz_len = quiz_len if len(pkList) > quiz_len else len(pkList)
        print('available was ' , pkList)
        for i in range(len(pkList) - quiz_len):
            randId = choice(pkList)
            pkList.remove(randId)



        print('after removing random questions is now ' , pkList)
        #print("Choices", question.choices.all())
        #modify each question to limit their choice list to 4 randoms
        available = available.filter(id__in=pkList)

        return available






    def list(self,request):
        serializer = QuestionSerializer(self.get_queryset(), many= True)

        return Response({"question_batch" : serializer.data})
