import pandas as pd
from django.core.management.base import BaseCommand
from trivia_game import models
from annoying.functions import get_object_or_None
from django.db import transaction
import os
from django.conf import settings
from django.db.models import Q

####################################
#  TEST/CODE CHANGING, ADDING, DELETING, AND POSSIBLY MOVING ENTRIES IN EXCEL AND THE ABILITY OF THE DB TO REACT PROPERLY


'''
LOOK THROUGH EACH ROW
CHECK EACH ATTR IN EACH CHOICE
IF THERE IS A CHANGE IN ATTR FOR CHOICE:
    THEN UPDATE IT TO THE DB AND ADD IT TO A LIST OF CHANGED CHOICES

DO THE SAME FOR CATEGORIES AND QUESTIONS;

AFTER GETTING TWO LISTS OF THE CHOICES AND QUESTIONS THAT HAVE BEEN updated
    LOOK THROUGH EACH LIST FOR CHOICES\QUESTIONS THAT MATCH GENDER AND ANSWER TYPE
        IF DIFFICULTY > 1 THEN MATCH TIME PERIOD TOO UNLESS TP FOR THE QUESTION IS *
'''
####################################



class UnevenDataException(Exception):
    pass


class Command(BaseCommand):
    args = '<excel file name>'
    help = 'updates database with new trivia info in excel spreadsheet'



    def print_links(self,model = None):

        if model is None:
            for q in models.Question.objects.all():

                print("--------------" + str(q) + "---------------")

                for choice in q.choices.all():
                    print(choice.id)

                print("Correct_Answer:" + str(q.correct_answer))

                print("------------------------------------")



        else:

            print("--------------" + str(model) + "---------------")

            if isinstance(model,models.Question):

                for choice in model.choices.all():
                    print(choice.id)
                print("Correct_Answer:" + str(model.correct_answer))

            elif  isinstance(model,models.Choice):
                for question in model.question_set.all():
                    print(question)
                print("Questions using this choice as an answer...")
                for question in model.accurate_questions.all():
                    print(question)

            print("------------------------------------")

    def update_model_atts(self, model_instance, xl_page, row_i, new_instance = False):

        updated = False
        db_dict = model_instance.to_dict()
        if new_instance:
            for att_name in db_dict:
                xl_val = self.clean_input(model_instance, att_name, xl_page.loc[row_i, att_name.upper()])

                setattr(model_instance, att_name, xl_val)

            model_instance.save()
            updated = True
        else:


            for att_name in db_dict:
                val = db_dict[att_name]
                xl_val = self.clean_input(model_instance, att_name, xl_page.loc[row_i, att_name.upper()])

                if val != xl_val:
                    setattr(model_instance, att_name, xl_val)
                    model_instance.save()
                    print("model: " + model_instance.__class__.__name__ + " updated " + str(model_instance))
                    updated = True


        return (model_instance, updated)


    def filter_and_remove_questions(self,choice):



        #is_hard = ~Q(categories__difficulty = '1')
        query = Q(categories__answer_type = choice.answer_type)
        if choice.gender != "*":
            query &= Q(categories__gender = choice.gender)
            #is_hard &= Q(categories__time_period = choice.time_period)

        #is_easy = Q(categories__difficulty = '1')



        #query  &= (is_hard | is_easy)




        if len(choice.question_set.all()) > 0:
            l = len(choice.question_set.all())


            set = choice.question_set.exclude(query)


            choice.question_set.remove(*set)
            if len(choice.question_set.all()) != l:
                print("removed link(s)")

        related_qs = models.Question.objects.filter(query)

        return related_qs

    def filter_and_remove_choices(self, question):

        query = Q(answer_type = question.categories.answer_type)

        #if question.categories.difficulty != '1':

            #query &= (Q(time_period = question.categories.time_period) | Q(time_period = "*"))

        if question.categories.gender != "*":
            query &= Q(gender = question.categories.gender)

        if len(question.choices.all()) > 0:
            l = len(question.choices.all())


            set = question.choices.exclude(query)

            question.choices.remove(*set)
            if len(question.choices.all()) != l:
                print("removed links between Q-" + str(question.id) + " and " + str(set))
        related_choices = models.Choice.objects.filter(query)

        return related_choices




    def clean_input(self, model, field_name, input):
        field = getattr(model,field_name)
        output = None

        if type(field) is bool:

            output = True if input == "X" else False

        elif field_name == "correct_answer":
            output = models.Choice.objects.get(pk = int(input))

        else:
            output = input
            print(field_name, output)
        return output



    def update_links(self, updated_qs, updated_choices):

        if len(updated_qs) > 0:
            for question in updated_qs:

                related_choices = self.filter_and_remove_choices(question)

                for x in related_choices:
                    if not question.choices.filter(id= x.id).exists():
                        question.choices.add(x)
                        print("added link from question:" + str(question.id) + " -> " + str(x.id))

                #self.print_links(question)


        if len(updated_choices) > 0:

            for choice in updated_choices:

                related_qs = self.filter_and_remove_questions(choice)
                for x in related_qs:
                    if not choice.question_set.filter(id = x.id).exists():
                        choice.question_set.add(x)
                        #print("added link from choice:" + str(choice) + " -> " + str(x) + "\n****************************\n")




    def add_new_question(self,question_info, linked_c, row_i):
        new_question = models.Question.objects.create(id = int(question_info.loc[row_i, "QUESTION_ID"]),
        categories = linked_c)
        (q, updated) = self.update_model_atts(new_question, question_info, row_i, new_instance = True)
        print("created new question:" + str(new_question))
        return q



    def add_new_category(self,question_info,row_i):

        question_category = models.QuestionCategory.objects.create()
        (cat, updated) = self.update_model_atts(question_category, question_info, row_i,new_instance = True)
        print("added new category ->" + str(question_category))

        return cat


    def add_new_choice(self,choice_info, row_i):
        new_choice = models.Choice.objects.create(id = int(choice_info.loc[row_i, "CHOICE_ID"]))
        (c, updated) = self.update_model_atts(new_choice, choice_info, row_i,new_instance = True)
        print("added new choice -> " + str(c))
        return c

    def update_question_info(self,question_info):

            recently_updated_qs = []

            for row_i in range(question_info.shape[0]):

                db_question = get_object_or_None(models.Question, id = int(question_info.loc[row_i, "QUESTION_ID"]))


                if db_question != None:

                    self.update_model_atts(db_question, question_info, row_i)

                    (updated_cat,has_updated) = self.update_model_atts(db_question.categories, question_info, row_i)


                    if has_updated:
                        recently_updated_qs.append(db_question) ########

                else:

                    new_question_category = self.add_new_category(question_info,row_i)
                    new_question = self.add_new_question(question_info,new_question_category,row_i)

                    recently_updated_qs.append(new_question) #############


            return recently_updated_qs





    def update_choices(self,choice_info):
            #CHOICES

            recently_updated = []

            for row_i in range(choice_info.shape[0]):

                #choice_entry = get_object_or_None(models.Choice, choice_text = choice_info.loc[i,"CHOICE_TEXT"])
                choice_entry = get_object_or_None(models.Choice, id = int(choice_info.loc[row_i, "CHOICE_ID"]))

                if choice_entry != None:
                    (updated_choice,has_updated) = self.update_model_atts(choice_entry, choice_info, row_i)
                    if has_updated:
                        recently_updated.append(updated_choice) ## or choice_entry

                else:

                    new_choice = self.add_new_choice(choice_info, row_i)
                    recently_updated.append(new_choice)


            return recently_updated





    @transaction.atomic
    def _update_db(self):

        #self.print_links()

        file_path =  settings.DB_URL


        if not os.path.exists(file_path):
            raise FileNotFoundError("Couldn't find database excel")



        question_info = pd.read_excel(file_path, sheet_name="Questions", dtype= str)
        choice_info = pd.read_excel(file_path, sheet_name = "Choices" , dtype = str)


        updated_choices = self.update_choices(choice_info)

        updated_qs = self.update_question_info(question_info)

        self.update_links(updated_qs, updated_choices)


    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        self._update_db()
