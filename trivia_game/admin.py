from django.contrib import admin

from .models import Choice, Question,QuestionCategory

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(QuestionCategory)
