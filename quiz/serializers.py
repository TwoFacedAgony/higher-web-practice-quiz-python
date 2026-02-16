"""Сериализаторы для моделей приложения quiz."""

from rest_framework import serializers

from quiz.models import Category, Question, Quiz


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Question."""

    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Quiz."""

    class Meta:
        model = Quiz
        fields = '__all__'
