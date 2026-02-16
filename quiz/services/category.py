"""Модуль с реализацией сервиса категорий"""

from quiz.dao import AbstractCategoryService
from quiz.models import Category


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
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None

    def create_category(self, title: str) -> Category:
        """
        Создаёт новую категорию.

        :param title: Название категории.
        :return: Созданный объект Category.
        """
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict) -> Category | None:
        """
        Обновляет существующую категорию.

        :param category_id: Идентификатор категории.
        :param data: Словарь с полями для обновления.
        :return: Обновлённый объект Category или None, если категории нет.
        """
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    def delete_category(self, category_id: int) -> None:
        """
        Удаляет категорию по идентификатору.

        :param category_id: Идентификатор категории.
        """
        Category.objects.filter(pk=category_id).delete()
