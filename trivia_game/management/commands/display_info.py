from django.core.management.base import BaseCommand
from trivia_game import models
from django.db import transaction
import django.db.models as django_models
class Command(BaseCommand):
    args = '<excel file name>'
    help = 'updates database with new trivia info in excel spreadsheet'





    def _display_info(self):

        choice_selector = {
        "time_period" : "O",
        "answer_type" : "DO",
        "gender" : "M"
        }

        question_selector = {
        "difficulty" : "1",
        "time_period" : "O",
        "answer_type" : "NA",
        "category" : "jesus"
        }

        model = "A"


        if(model == "C"):

            '''
            for at in models.AnswerType.ANSWER_TYPES:

                current_at = at[0]

                at_count = models.Choice.objects.filter(answer_type=current_at).count()
                print("Number of answer choices for answer type:" + at[1] + " is " + str(at_count))

                '''

            for c in models.Choice.objects.filter(answer_type="DO"):
                print(c.choice_text)

        elif(model == "Q"):
            field_names = [field.name for field in models.QuestionCategory._meta.get_fields()]
            for field_name in field_names:

                if(type(models.QuestionCategory._meta.get_field(field_name)) is django_models.BooleanField):
                    val = True
                    print("Number of questions with the selector:" + field_name + " is " + str(models.QuestionCategory.objects.filter(**{field_name : val}).count()))

        elif(model=="A"):
            buggy = models.Question.objects.filter(pk__in=[3,8,10])
            for q in models.Question.objects.all():
                print(q.question_text,len(q.choices.all()))




    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):

        self._display_info()
