"""Валидаторы для моделей приложения quiz."""

from django.core.exceptions import ValidationError


def validate_answer_options(options):
    """
    Проверяет, что варианты ответов являются списком/кортежем,
    содержат не менее двух элементов, и все элементы одного типа
    (числа или строки).

    :param options: Проверяемое значение (ожидается список или кортеж).
    :raises ValidationError: Если значение не соответствует требованиям.
    """
    if not type(options) is (list, tuple):
        raise ValidationError('Answer options must be a list or a tuple')

    if len(options) < 2:
        raise ValidationError(
            'Question must have at least two possible answers'
        )

    if not (
        all(type(answer) in (int, float) for answer in options)
        or all(type(answer) is str for answer in options)
    ):
        raise ValidationError('All answers must be numbers or strings')
