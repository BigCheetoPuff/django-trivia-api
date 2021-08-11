from django.db import models

from django_random_queryset import RandomManager
############################# DJANGO CASCADE DOESNT WORK QUESTION DOENST DEL CAT
class AnswerType:
    ANSWER_TYPES = [
    ("N", "NAME"),
    ("PL", "PLACE"),
    ("R","REASON"),
    ("I","ITEM"),
    ("AN","ANIMAL"),
    ("PE" , "PERSON"),
    ("NU" , "NUMBER"),
    ("DO", "DOCTRINE"),

    ]

    DIFFICULTY_CHOICES = [
    ("1","EASY"),
    ("2","MEDIUM"),
    ("3", "HARD")
    ]

    TIME_PERIOD = [
    ("O", "OLD TESTAMENT"),
    ("N", "NEW TESTAMENT"),
    ("*", "N/A")
    ]

    GENDER = [
    ("M" , "MALE"),
    ("F", "FEMALE"),
    ("*", "N/A")
    ]


class Choice(models.Model):
    objects = RandomManager()

    choice_text = models.CharField(max_length = 200)
    #description = models.CharField(max_length = 400)
    time_period = models.CharField(max_length= 10,
    choices= AnswerType.TIME_PERIOD, default = "X")

    answer_type = models.CharField(max_length = 10,
    choices = AnswerType.ANSWER_TYPES)

    gender = models.CharField(max_length = 10,
    choices = AnswerType.GENDER, default = "*")

    def to_dict(self):
        return {
        "choice_text" : self.choice_text,
        #"description" : self.description,
        "time_period" : self.time_period,
        "answer_type" : self.answer_type,
        "gender": self.gender
        }

    def __str__(self):
        return "<" + str(self.id) + ":" + str(self.to_dict()) +  ">"


    class Meta:
        ordering = ['id']

class QuestionCategory(models.Model):


    difficulty = models.CharField(max_length = 10,
    choices = AnswerType.DIFFICULTY_CHOICES,
    default = 1)


    answer_type = models.CharField(max_length = 10,
    choices = AnswerType.ANSWER_TYPES)

    time_period = models.CharField(max_length = 1,
    choices = AnswerType.TIME_PERIOD, default = "X")

    gender = models.CharField(max_length = 10,
    choices = AnswerType.GENDER, default = "*")

    jesus = models.BooleanField(default = False)
    doctrine = models.BooleanField(default = False)
    prophecy =  models.BooleanField(default = False)
    geneology=  models.BooleanField(default = False)
    gospel = models.BooleanField(default = False)
    miracle =  models.BooleanField(default = False)
    history =  models.BooleanField(default = False)

    def to_dict(self):
        return {
        "difficulty" : self.difficulty,
        "time_period" : self.time_period,
        "gender": self.gender,
        "answer_type" : self.answer_type,
        "jesus" : self.jesus,
        "doctrine" : self.doctrine,
        "prophecy" : self.prophecy,
        "geneology" : self.geneology,
        "gospel" : self.gospel,
        "miracle" : self.miracle,
        "history" : self.history
        }


    def __str__(self):
        return str(self.to_dict())

    class Meta:
        ordering = ["question"]


class Question(models.Model):



    question_text = models.CharField(max_length = 300)

    choices = models.ManyToManyField(Choice, max_length = 200)

    correct_answer = models.ForeignKey(Choice, related_name="accurate_questions",
    on_delete = models.SET_NULL,
    null = True,
    blank = True
    )

    categories = models.OneToOneField(QuestionCategory,
    on_delete = models.CASCADE)




    def __str__(self):
        return "<" + str(self.id) + ":" + self.question_text + str(self.categories.to_dict()) + " Correct answer : " + str(self.correct_answer) + ">"

    def to_dict(self):
        return {
        "question_text": self.question_text,
        "correct_answer" : self.correct_answer
        }

    class Meta:
        ordering = ['id']
