"""Модуль с представлениями для работы с вопросами"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class QuestionCRUDApiView(APIView):
    """Представление для операций CRUD с вопросами."""

    serializer_class = QuestionSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuestionService()

    def get(self, request, question_id=None):
        """
        Обрабатывает GET-запросы.

        Если указан question_id — возвращает конкретный вопрос,
        иначе — список всех вопросов.

        :param request: Объект запроса.
        :param question_id: Идентификатор вопроса (опционально).
        :return: Response с данными вопроса(ов) или 404.
        """
        if question_id is not None:
            question = self.service.get_question(question_id)
            if not question:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(question)
            return Response(serializer.data, status=status.HTTP_200_OK)

        questions = self.service.list_questions()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Обрабатывает POST-запрос на создание вопроса.

        :param request: Объект запроса с данными.
        :return: Response с созданным вопросом и статусом 201.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        quiz_id = validated['quiz'].id
        data = {k: v for k, v in validated.items() if k != 'quiz'}

        question = self.service.create_question(quiz_id, data)
        response_serializer = self.serializer_class(question)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, question_id):
        """
        Обрабатывает PUT-запрос на обновление вопроса.

        :param request: Объект запроса с данными.
        :param question_id: Идентификатор вопроса.
        :return: Response с обновлённым вопросом или 404.
        """
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_question = self.service.update_question(
            question_id,
            serializer.validated_data
        )
        if not updated_question:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response_serializer = self.serializer_class(updated_question)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, question_id):
        """
        Обрабатывает DELETE-запрос на удаление вопроса.

        :param request: Объект запроса.
        :param question_id: Идентификатор вопроса.
        :return: Response со статусом 204 или 404.
        """
        question = self.service.get_question(question_id)
        if not question:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.service.delete_question(question_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionByTextApiView(APIView):
    """Представление для поиска вопросов по тексту."""

    serializer_class = QuestionSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuestionService()

    def get(self, request, query):
        """
        Возвращает вопросы, текст которых содержит подстроку query.

        :param request: Объект запроса.
        :param query: Подстрока для поиска.
        :return: Response со списком вопросов.
        """
        questions = self.service.get_questions_by_text(query)
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionAnswerApiView(APIView):
    """Представление для проверки ответа на вопрос."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuestionService()

    def post(self, request, question_id):
        """
        Проверяет ответ на указанный вопрос.

        :param request: Объект запроса, содержащий поле 'answer'.
        :param question_id: Идентификатор вопроса.
        :return: Response с полем 'correct' (true/false) или 404.
        """
        question = self.service.get_question(question_id)
        if not question:
            return Response(status=status.HTTP_404_NOT_FOUND)

        answer = request.data.get('answer', '')
        correct = self.service.check_answer(question_id, answer)
        return Response({'correct': correct}, status=status.HTTP_200_OK)
