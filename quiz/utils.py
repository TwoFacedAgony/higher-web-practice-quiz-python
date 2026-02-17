from django.shortcuts import get_object_or_404
from django.db import models


def update_object(model: models.Model, object_id: int, data: dict):
    """
    Функция для обновления объектов текущих моделей.

    :param model: Класс модели Django.
    :param object_id: Идентификатор объекта.
    :param data: Словарь с полями для обновления.
    :return: Обновлённый объект.
    :raises Http404: Если объект не найден.
    """
    obj = get_object_or_404(model, pk=object_id)
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
    return obj
