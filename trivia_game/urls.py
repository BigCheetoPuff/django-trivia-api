from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trivia_game import viewsets



router = DefaultRouter()
router.register(r'questions', viewsets.QuestionViewSet, basename = "Question")


urlpatterns = [

path('', include(router.urls)),


]
