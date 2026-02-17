"""Модуль с реализацией сервиса квизов"""
from django.shortcuts import get_object_or_404
from quiz.dao import AbstractQuizService
from quiz.models import Quiz
from quiz.utils import update_object


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза"""

    def list_quizzes(self) -> list[Quiz]:
        """
        Возвращает список всех квизов.

        :return: Список объектов Quiz.
        """
        return list(Quiz.objects.all())

    def get_quiz(self, quiz_id: int) -> Quiz | None:
        """
        Возвращает квиз по идентификатору.

        :param quiz_id: Идентификатор квиза.
        :return: Объект Quiz или None, если квиз не найден.
        """
        return get_object_or_404(Quiz, pk=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """
        Возвращает квизы, название которых содержит указанную подстроку.

        :param title: Подстрока для поиска.
        :return: Список подходящих квизов.
        """
        return list(Quiz.objects.filter(title__icontains=title))

    def get_quizzes_by_title(self, title: str) -> list[Quiz]:
        """Alias для совместимости с view."""
        return self.get_quizes_by_title(title)

    def create_quiz(self, data: dict) -> Quiz:
        """
        Создаёт новый квиз.

        :param data: Словарь с данными квиза.
        :return: Созданный объект Quiz.
        """
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz | None:
        """
        Обновляет существующий квиз.

        :param quiz_id: Идентификатор квиза.
        :param data: Словарь с полями для обновления.
        :return: Обновлённый объект Quiz или None, если квиз не найден.
        """
        return update_object(Quiz, quiz_id, data)

    def delete_quiz(self, quiz_id: int) -> None:
        """
        Удаляет квиз по идентификатору.

        :param quiz_id: Идентификатор квиза.
        """
        Quiz.objects.filter(pk=quiz_id).delete()
