"""Модуль с реализацией сервиса вопросов"""

import random
from django.shortcuts import get_object_or_404
from quiz.dao import AbstractQuestionService
from quiz.models import Question
from quiz.utils import update_object


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов"""

    def list_questions(self) -> list[Question]:
        """
        Возвращает список всех вопросов.

        :return: Список объектов Question.
        """
        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question | None:
        """
        Возвращает вопрос по идентификатору.

        :param question_id: Идентификатор вопроса.
        :return: Объект Question или None, если вопрос не найден.
        """
        return get_object_or_404(Question, pk=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """
        Возвращает вопросы, текст которых содержит указанную подстроку.

        :param text: Текст для поиска.
        :return: Список подходящих вопросов.
        """
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """
        Возвращает все вопросы, относящиеся к указанному квизу.

        :param quiz_id: Идентификатор квиза.
        :return: Список вопросов квиза.
        """
        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """
        Создаёт новый вопрос для указанного квиза.

        :param quiz_id: Идентификатор квиза.
        :param data: Словарь с полями вопроса (без поля quiz).
        :return: Созданный объект Question.
        """
        data = dict(data)
        data['quiz_id'] = quiz_id
        return Question.objects.create(**data)

    def update_question(self, question_id: int, data: dict) -> Question | None:
        """
        Обновляет существующий вопрос.

        :param question_id: Идентификатор вопроса.
        :param data: Словарь с полями для обновления.
        :return: Обновлённый объект Question или None, если вопрос не найден.
        """
        return update_object(Question, question_id, data)

    def delete_question(self, question_id: int) -> None:
        """
        Удаляет вопрос по идентификатору.

        :param question_id: Идентификатор вопроса.
        """
        Question.objects.filter(pk=question_id).delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        """
        Проверяет, является ли ответ правильным для указанного вопроса.

        :param question_id: Идентификатор вопроса.
        :param answer: Ответ пользователя.
        :return: True, если ответ совпадает с правильным, иначе False.
        """
        question = get_object_or_404(Question, pk=question_id)
        return question.correct_answer.strip() == answer.strip()

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """
        Возвращает случайный вопрос из указанного квиза.

        :param quiz_id: Идентификатор квиза.
        :return: Случайный объект Question.
        :raises ValueError: Если в квизе нет вопросов.
        """
        questions = self.get_questions_for_quiz(quiz_id)
        if not questions:
            raise ValueError('No questions found')
        return random.choice(questions)
