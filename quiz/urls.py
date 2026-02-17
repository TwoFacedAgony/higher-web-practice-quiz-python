"""Модуль с роутингом"""

from django.urls import include, path

from quiz.views.category import CategoryApiView as CategoryView
from quiz.views.question import (
    QuestionCRUDApiView,
    QuestionByTextApiView,
    QuestionAnswerApiView,
)
from quiz.views.quiz import (
    QuizCRUDApiView,
    QuizQuestionView,
    QuizByTitleView,
)

category_urls = [
    path('', CategoryView.as_view(), name='category_list'),
    path(
        '<int:category_id>/',
        CategoryView.as_view(),
        name='category_detail'
    ),
]

question_urls = [
    path(
        'by_text/<str:query>/',
        QuestionByTextApiView.as_view(),
        name='question_by_text'
    ),
    path(
        '<int:question_id>/check/',
        QuestionAnswerApiView.as_view(),
        name='question_answer'
    ),
    path(
        '<int:question_id>/',
        QuestionCRUDApiView.as_view(),
        name='question_detail'
    ),
    path('', QuestionCRUDApiView.as_view(), name='question_list'),
]

quiz_urls = [
    path(
        'by_title/<str:title>/',
        QuizByTitleView.as_view(),
        name='quiz_by_title'
    ),
    path(
        '<int:quiz_id>/random_question/',
        QuizQuestionView.as_view(),
        name='quiz_question'
    ),
    path(
        '<int:quiz_id>/',
        QuizCRUDApiView.as_view(),
        name='quiz_detail'
    ),
    path(
        '',
        QuizCRUDApiView.as_view(),
        name='quiz_list'
    ),
]

urlpatterns = [
    path('category/', include(category_urls)),
    path('question/', include(question_urls)),
    path('quiz/', include(quiz_urls)),
]
