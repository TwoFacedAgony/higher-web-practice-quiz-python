"""Модуль с представлениями для работы с категориями"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService


class CategoryApiView(APIView):
    """Представление для операций CRUD с категориями."""

    serializer_class = CategorySerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CategoryService()

    def get(self, request, category_id=None):
        """
        Обрабатывает GET-запросы.

        Если указан category_id — возвращает конкретную категорию,
        иначе — список всех категорий.

        :param request: Объект запроса.
        :param category_id: Идентификатор категории (опционально).
        :return: Response с данными категории(й) или 404.
        """
        if category_id is not None:
            category = self.service.get_category(category_id)
            if not category:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(category)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        categories = self.service.list_categories()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Обрабатывает POST-запрос на создание категории.

        :param request: Объект запроса с данными.
        :return: Response с созданной категорией и статусом 201.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data['title']
        category = self.service.create_category(title)
        response_serializer = self.serializer_class(category)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, category_id):
        """
        Обрабатывает PUT-запрос на обновление категории.

        :param request: Объект запроса с данными.
        :param category_id: Идентификатор категории.
        :return: Response с обновлённой категорией или 404.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_category = self.service.update_category(
            category_id,
            serializer.validated_data
        )
        if not updated_category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response_serializer = self.serializer_class(updated_category)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, category_id):
        """
        Обрабатывает DELETE-запрос на удаление категории.

        :param request: Объект запроса.
        :param category_id: Идентификатор категории.
        :return: Response со статусом 204 или 404.
        """
        category = self.service.get_category(category_id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.service.delete_category(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
