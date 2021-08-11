from rest_framework import serializers
from .models import Choice, Question, QuestionCategory


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id','choice_text','time_period','answer_type') # ,question_set


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ("id","difficulty","time_period","jesus","doctrine","prophecy","geneology","gospel","miracle","history")




class QuestionSerializer(serializers.ModelSerializer):
    #choices = ChoiceSerializer(many = True, read_only = True)
    correct_answer = ChoiceSerializer(read_only = True)
    categories = QuestionCategorySerializer(read_only = True)

    chosen_choices = serializers.SerializerMethodField("get_chosen_choices")

    def get_chosen_choices(self, obj):
        correct_query = obj.choices.filter(pk= obj.correct_answer.pk)
        output_choices = obj.choices.exclude(pk= obj.correct_answer.pk).random(3).union(correct_query)
        return ChoiceSerializer(output_choices, many=True).data





    class Meta:
        model = Question
        fields = ("id","question_text","chosen_choices","correct_answer","categories")
