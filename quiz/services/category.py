"""Модуль с реализацией сервиса категорий"""
from rest_framework.generics import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category
from quiz.utils import update_object


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий"""

    def list_categories(self) -> list[Category]:
        """
        Возвращает список всех категорий.

        :return: Список объектов Category.
        """
        return list(Category.objects.all())

    def get_category(self, category_id: int) -> Category | None:
        """
        Возвращает категорию по идентификатору.

        :param category_id: Идентификатор категории.
        :return: Объект Category или None, если категория не найдена.
        """
        return get_object_or_404(Category, pk=category_id)

    def create_category(self, title: str) -> Category:
        """
        Создаёт новую категорию.

        :param title: Название категории.
        :return: Созданный объект Category.
        """
        category, _ = Category.objects.get_or_create(title=title)
        return category

    def update_category(self, category_id: int, data: dict) -> Category:
        """
        Обновляет существующую категорию.

        :param category_id: Идентификатор категории.
        :param data: Словарь с полями для обновления.
        :return: Обновлённый объект Category или None, если категории нет.
        """
        return update_object(Category, category_id, data)

    def delete_category(self, category_id: int) -> None:
        """
        Удаляет категорию по идентификатору.

        :param category_id: Идентификатор категории.
        """
        Category.objects.filter(pk=category_id).delete()
