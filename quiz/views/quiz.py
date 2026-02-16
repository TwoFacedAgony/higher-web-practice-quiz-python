"""Модуль с представлениями для работы с квизами"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuizSerializer, QuestionSerializer
from quiz.services.quiz import QuizService
from quiz.services.question import QuestionService


class QuizCRUDApiView(APIView):
    """Представление для операций CRUD с квизами."""

    serializer_class = QuizSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuizService()

    def get(self, request, quiz_id=None):
        """
        Обрабатывает GET-запросы.

        Если указан quiz_id — возвращает конкретный квиз,
        иначе — список всех квизов.

        :param request: Объект запроса.
        :param quiz_id: Идентификатор квиза (опционально).
        :return: Response с данными квиза(ов) или 404.
        """
        if quiz_id is not None:
            quiz = self.service.get_quiz(quiz_id)
            if not quiz:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)

        quizzes = self.service.list_quizzes()
        serializer = self.serializer_class(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Обрабатывает POST-запрос на создание квиза.

        :param request: Объект запроса с данными.
        :return: Response с созданным квизом и статусом 201.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz = self.service.create_quiz(serializer.validated_data)
        response_serializer = self.serializer_class(quiz)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, quiz_id):
        """
        Обрабатывает PUT-запрос на обновление квиза.

        :param request: Объект запроса с данными.
        :param quiz_id: Идентификатор квиза.
        :return: Response с обновлённым квизом или 404.
        """
        serializer = self.serializer_class(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        updated_quiz = self.service.update_quiz(
            quiz_id,
            serializer.validated_data
        )
        if not updated_quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response_serializer = self.serializer_class(updated_quiz)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, quiz_id):
        """
        Обрабатывает DELETE-запрос на удаление квиза.

        :param request: Объект запроса.
        :param quiz_id: Идентификатор квиза.
        :return: Response со статусом 204 или 404.
        """
        quiz = self.service.get_quiz(quiz_id)
        if not quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.service.delete_quiz(quiz_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizQuestionView(APIView):
    """Представление для получения случайного вопроса из квиза."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quiz_service = QuizService()
        self.question_service = QuestionService()

    def get(self, request, quiz_id):
        """
        Возвращает случайный вопрос из указанного квиза.

        :param request: Объект запроса.
        :param quiz_id: Идентификатор квиза.
        :return: Response с данными вопроса или 404.
        """
        quiz = self.quiz_service.get_quiz(quiz_id)
        if not quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            question = self.question_service.random_question_from_quiz(quiz_id)
        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizByTitleView(APIView):
    """Представление для поиска квизов по названию."""

    serializer_class = QuizSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuizService()

    def get(self, request, title):
        """
        Возвращает квизы, название которых содержит подстроку title.

        :param request: Объект запроса.
        :param title: Подстрока для поиска.
        :return: Response со списком квизов.
        """
        quizzes = self.service.get_quizzes_by_title(title)
        serializer = self.serializer_class(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
