"""Модуль с настройками административной панели для моделей quiz"""

from django.contrib import admin

from quiz.constants import MAX_STR_RETURN_LENGTH
from quiz.models import Category, Question, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Category."""

    list_display = (
        'id',
        'title'
    )
    search_fields = (
        'title',
    )
    empty_value_display = '-empty-'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Quiz."""

    list_display = (
        'id',
        'title',
        'short_description'
    )
    search_fields = (
        'title',
    )
    empty_value_display = '-empty-'

    @admin.display(description='Description')
    def short_description(self, obj):
        """
        Возвращает сокращённое описание квиза.

        :param obj: Объект Quiz.
        :return: Усечённая строка описания или '-empty-'.
        """
        if obj.description:
            return obj.description[:MAX_STR_RETURN_LENGTH]
        return '-empty-'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Question."""

    list_display = (
        'id',
        'short_text',
        'category',
        'quiz',
        'difficulty',
        'short_options',
        'short_correct_answer',
        'short_explanation'
    )
    list_editable = (
        'difficulty',
        'category',
        'quiz',
    )
    search_fields = (
        'text',
        'options',
        'correct_answer',
        'explanation',
        'category__title',
        'quiz__title'
    )
    list_filter = (
        'difficulty',
        'category',
        'quiz',
    )
    list_select_related = (
        'category',
        'quiz',
    )
    empty_value_display = '-empty-'

    @admin.display(description='Текст вопроса')
    def short_text(self, obj):
        """
        Возвращает сокращённый текст вопроса.

        :param obj: Объект Question.
        :return: Усечённая строка текста.
        """
        return obj.text[:MAX_STR_RETURN_LENGTH]

    @admin.display(description='Варианты ответов')
    def short_options(self, obj):
        """
        Возвращает сокращённые варианты ответов.

        :param obj: Объект Question.
        :return: Усечённая строка options.
        """
        return obj.options[:MAX_STR_RETURN_LENGTH]

    @admin.display(description='Правильный ответ')
    def short_correct_answer(self, obj):
        """
        Возвращает сокращённый правильный ответ.

        :param obj: Объект Question.
        :return: Усечённая строка correct_answer.
        """
        return obj.correct_answer[:MAX_STR_RETURN_LENGTH]

    @admin.display(description='Пояснение')
    def short_explanation(self, obj):
        """
        Возвращает сокращённое пояснение к ответу.

        :param obj: Объект Question.
        :return: Усечённая строка explanation или '-empty-'.
        """
        if obj.explanation:
            return obj.explanation[:MAX_STR_RETURN_LENGTH]
        return '-empty-'
