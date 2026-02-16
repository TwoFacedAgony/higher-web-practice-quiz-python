"""Модуль с роутингом"""

#### Category

# - POST `/api/category` - создание категории
# - GET `/api/category` - получение всех категории
# - GET `/api/category/<int:id>` - получение категории по идентификатору
# - PUT `/api/category/<int:id>` - изменение категории
# - DELETE `/api/category/<int:id>` - удаление категории


#### Question

# - POST `/api/question` - создание вопроса
# - GET `/api/question` - получение всех вопросов
# - GET `/api/question/<int:id>` - получение вопроса по идентификатору
# - GET `/api/question/by_text/<str:text>` - получение вопроса по тексту
# - POST `/api/question/<int:id>/check` - проверка ответа на вопрос
# - PUT `/api/question/<int:id>` - изменение вопроса
# - DELETE `/api/question/<int:id>` - удаление вопроса


#### Quiz

# - POST `/api/quiz` - создание квиза
# - GET `/api/quiz` - получение всех квизов
# - GET `/api/quiz/<int:id>` - получение квиза по идентификатору
# - GET `/api/quiz/<int:id>/random_question` - получение случайного вопроса по идентификатору квиза
# - GET `/api/quiz/by_title/<str:title>` - получение квиза по названию
# - PUT `/api/quiz/<int:id>` - изменение квиза
# - DELETE `/api/quiz/<int:id>` - удаление квиза


# Сюда добавляем все пути и их обработчики

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
