"""Модели данных для приложения quiz."""

from django.db import models

from quiz.constants import (
    MAX_CATEGORY_TITLE_LENGTH,
    MAX_QUIZ_TITLE_LENGTH,
    MAX_QUIZ_DESCRIPTION_LENGTH,
    MAX_STR_RETURN_LENGTH,
    MAX_QUESTION_DESCRIPTION_LENGTH,
    MAX_QUESTION_TEXT_LENGTH,
    MAX_QUESTION_EXPLANATION_LENGTH
)
from quiz.validators import validate_answer_options


class Category(models.Model):
    """Модель категории вопросов."""

    title = models.CharField(
        max_length=MAX_CATEGORY_TITLE_LENGTH,
        unique=True,
        blank=False,
        verbose_name='category title',
    )

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        ordering = (
            'title',
        )

    def __str__(self):
        return self.title[:MAX_STR_RETURN_LENGTH]


class Quiz(models.Model):
    """Модель квиза (теста/викторины)."""

    title = models.CharField(
        max_length=MAX_QUIZ_TITLE_LENGTH,
        unique=True,
        null=False,
        verbose_name='quiz title',
    )
    description = models.TextField(
        max_length=MAX_QUIZ_DESCRIPTION_LENGTH,
        null=True,
        blank=True,
        verbose_name='quiz description',
    )

    class Meta:
        verbose_name_plural = 'Quizzes'
        verbose_name = 'Quiz'
        ordering = (
            'title',
        )

    def __str__(self):
        return self.title[:MAX_STR_RETURN_LENGTH]


class Difficulty(models.TextChoices):
    """Перечисление уровней сложности вопроса."""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'

    def __str__(self):
        return 'Difficulty choices: EASY, MEDIUM, HARD'


class Question(models.Model):
    """Модель вопроса."""

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='category',
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='quiz'
    )
    description = models.TextField(
        max_length=MAX_QUESTION_DESCRIPTION_LENGTH,
        null=True,
        blank=True,
        verbose_name='description',
    )
    text = models.TextField(
        max_length=MAX_QUESTION_TEXT_LENGTH,
        verbose_name='text',
    )
    options = models.TextField(
        verbose_name='answer options',
        validators=(
            validate_answer_options,
        )
    )
    correct_answer = models.TextField(
        verbose_name='correct answer',
    )
    explanation = models.TextField(
        max_length=MAX_QUESTION_EXPLANATION_LENGTH,
        blank=True,
        null=True,
        verbose_name='answer explanation',
    )
    difficulty = models.CharField(
        choices=Difficulty.choices,
        verbose_name='difficulty options',
    )

    class Meta:
        default_related_name = 'questions'
        verbose_name_plural = 'Questions'
        verbose_name = 'Question'
        ordering = (
            'difficulty',
        )
