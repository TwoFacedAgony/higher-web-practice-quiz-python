"""Тесты для API представлений приложения quiz."""

import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from quiz.models import Category, Quiz, Question, Difficulty


@pytest.fixture
def api_client():
    """Возвращает экземпляр APIClient для тестирования API."""
    return APIClient()


@pytest.mark.django_db
class TestCategoryAPI:
    """Тесты API категорий."""

    def test_create_category(self, api_client) -> None:
        """Тестирует создание категории через POST-запрос."""
        url = reverse('category_list')
        response = api_client.post(url, {'title': 'History'}, format='json')
        assert response.status_code == 201
        assert response.json()['title'] == 'History'

    def test_list_categories(self, api_client) -> None:
        """Тестирует получение списка всех категорий через GET-запрос."""
        Category.objects.create(title='A')
        Category.objects.create(title='B')
        url = reverse('category_list')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        titles = [c['title'] for c in data]
        assert 'A' in titles and 'B' in titles

    def test_get_category_by_id(self, api_client) -> None:
        """Тестирует получение конкретной категории по её ID."""
        category = Category.objects.create(title='Science')
        url = reverse('category_detail', kwargs={'category_id': category.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json()['title'] == 'Science'

    def test_get_category_404(self, api_client) -> None:
        """
        Тестирует, что GET-запрос к несуществующей категории возвращает 404.
        """
        url = reverse('category_detail', kwargs={'category_id': 99999})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_update_category(self, api_client) -> None:
        """Тестирует обновление категории через PUT-запрос."""
        category = Category.objects.create(title='Old')
        url = reverse('category_detail', kwargs={'category_id': category.id})
        response = api_client.put(url, {'title': 'New'}, format='json')
        assert response.status_code == 200
        assert response.json()['title'] == 'New'

    def test_update_category_404(self, api_client) -> None:
        """
        Тестирует, что PUT-запрос к несуществующей категории возвращает 404.
        """
        url = reverse('category_detail', kwargs={'category_id': 99999})
        response = api_client.put(url, {'title': 'New'}, format='json')
        assert response.status_code == 404

    def test_delete_category(self, api_client) -> None:
        """Тестирует удаление категории через DELETE-запрос."""
        category = Category.objects.create(title='To Delete')
        url = reverse('category_detail', kwargs={'category_id': category.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Category.objects.filter(pk=category.id).exists()

    def test_delete_category_404(self, api_client) -> None:
        """
        Тестирует, что DELETE-запрос к несуществующей категории возвращает 404.
        """
        url = reverse('category_detail', kwargs={'category_id': 99999})
        response = api_client.delete(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestQuizAPI:
    """Тесты API квизов."""

    def test_create_quiz(self, api_client) -> None:
        """Тестирует создание квиза через POST-запрос."""
        url = reverse('quiz_list')
        response = api_client.post(
            url,
            {'title': 'Math Quiz', 'description': 'About numbers'},
            format='json',
        )
        assert response.status_code == 201
        data = response.json()
        assert data['title'] == 'Math Quiz'
        assert data['description'] == 'About numbers'

    def test_list_quizzes(self, api_client) -> None:
        """Тестирует получение списка всех квизов через GET-запрос."""
        Quiz.objects.create(title='Quiz A')
        Quiz.objects.create(title='Quiz B')
        url = reverse('quiz_list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_quiz_by_id(self, api_client) -> None:
        """Тестирует получение конкретного квиза по его ID."""
        quiz = Quiz.objects.create(title='My Quiz', description='Desc')
        url = reverse('quiz_detail', kwargs={'quiz_id': quiz.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json()['title'] == 'My Quiz'

    def test_get_quiz_404(self, api_client) -> None:
        """Тестирует, что GET-запрос к несуществующему квизу возвращает 404."""
        url = reverse('quiz_detail', kwargs={'quiz_id': 99999})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_update_quiz(self, api_client) -> None:
        """Тестирует обновление квиза через PUT-запрос."""
        quiz = Quiz.objects.create(title='Old')
        url = reverse('quiz_detail', kwargs={'quiz_id': quiz.id})
        response = api_client.put(
            url,
            {'title': 'New', 'description': 'New desc'},
            format='json',
        )
        assert response.status_code == 200
        assert response.json()['title'] == 'New'

    def test_delete_quiz(self, api_client) -> None:
        """Тестирует удаление квиза через DELETE-запрос."""
        quiz = Quiz.objects.create(title='To Delete')
        url = reverse('quiz_detail', kwargs={'quiz_id': quiz.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Quiz.objects.filter(pk=quiz.id).exists()

    def test_get_quiz_by_title(self, api_client) -> None:
        """Тестирует поиск квизов по части названия через GET-запрос."""
        Quiz.objects.create(title='Python Basics')
        Quiz.objects.create(title='Python Advanced')
        url = reverse('quiz_by_title', kwargs={'title': 'Python'})
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        titles = [q['title'] for q in data]
        assert 'Python Basics' in titles and 'Python Advanced' in titles

    def test_random_question_from_quiz(self, api_client) -> None:
        """Тестирует получение случайного вопроса из квиза через GET-запрос."""
        quiz = Quiz.objects.create(title='Test')
        Question.objects.create(
            quiz=quiz,
            text='Q1',
            options='["A","B"]',
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        url = reverse('quiz_question', kwargs={'quiz_id': quiz.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json()['text'] == 'Q1'

    def test_random_question_404_when_no_questions(self, api_client) -> None:
        """
        Тестирует, что запрос случайного вопроса из пустого квиза
        возвращает ошибку 404.
        """
        quiz = Quiz.objects.create(title='Empty')
        url = reverse('quiz_question', kwargs={'quiz_id': quiz.id})
        response = api_client.get(url)
        assert response.status_code == 404


def _question_payload(quiz_id: int, **overrides) -> dict:
    """
    Возвращает словарь с данными для создания вопроса через API.

    :param quiz_id: Идентификатор квиза.
    :param overrides: Дополнительные поля для переопределения.
    :return: Словарь, готовый для передачи в запрос.
    """
    payload = {
        'quiz': quiz_id,
        'text': 'What is 2+2?',
        'options': json.dumps(['3', '4', '5']),
        'correct_answer': '4',
        'difficulty': Difficulty.EASY,
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestQuestionAPI:
    """Тесты API вопросов."""

    def test_list_questions(self, api_client) -> None:
        """Тестирует получение списка всех вопросов через GET-запрос."""
        quiz = Quiz.objects.create(title='Quiz')
        Question.objects.create(
            quiz=quiz,
            text='Q1',
            options='["A","B"]',
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_question_by_id(self, api_client) -> None:
        """Тестирует получение конкретного вопроса по его ID."""
        quiz = Quiz.objects.create(title='Quiz')
        q = Question.objects.create(
            quiz=quiz,
            text='Unique question text',
            options='["A","B"]',
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_detail', kwargs={'question_id': q.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json()['text'] == 'Unique question text'

    def test_get_question_404(self, api_client) -> None:
        """
        Тестирует, что GET-запрос к несуществующему вопросу возвращает 404.
        """
        url = reverse('question_detail', kwargs={'question_id': 99999})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_get_questions_by_text(self, api_client) -> None:
        """Тестирует поиск вопросов по части текста через GET-запрос."""
        quiz = Quiz.objects.create(title='Quiz')
        Question.objects.create(
            quiz=quiz,
            text='Searchable phrase in question',
            options='["A","B"]',
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_by_text', kwargs={'query': 'Searchable'})
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any('Searchable' in q['text'] for q in data)

    def test_check_answer_correct(self, api_client) -> None:
        """Тестирует проверку правильного ответа через POST-запрос."""
        quiz = Quiz.objects.create(title='Quiz')
        q = Question.objects.create(
            quiz=quiz,
            text='Q',
            options='["A","B"]',
            correct_answer='B',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_answer', kwargs={'question_id': q.id})
        response = api_client.post(url, {'answer': 'B'}, format='json')
        assert response.status_code == 200
        assert response.json()['correct'] is True

    def test_check_answer_incorrect(self, api_client) -> None:
        """Тестирует проверку неправильного ответа через POST-запрос."""
        quiz = Quiz.objects.create(title='Quiz')
        q = Question.objects.create(
            quiz=quiz,
            text='Q',
            options='["A","B"]',
            correct_answer='B',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_answer', kwargs={'question_id': q.id})
        response = api_client.post(url, {'answer': 'A'}, format='json')
        assert response.status_code == 200
        assert response.json()['correct'] is False

    def test_check_answer_404(self, api_client) -> None:
        """Тестирует, что для несуществующего вопроса возвращается 404."""
        url = reverse('question_answer', kwargs={'question_id': 99999})
        response = api_client.post(url, {'answer': 'X'}, format='json')
        assert response.status_code == 404

    def test_update_question(self, api_client) -> None:
        """Тестирует обновление вопроса через PUT-запрос."""
        quiz = Quiz.objects.create(title='Quiz')
        q = Question.objects.create(
            quiz=quiz,
            text='Original',
            options='["A","B"]',
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_detail', kwargs={'question_id': q.id})
        response = api_client.put(url, {'text': 'Updated'}, format='json')
        assert response.status_code == 200
        assert response.json()['text'] == 'Updated'

    def test_delete_question(self, api_client) -> None:
        """Тестирует удаление вопроса через DELETE-запрос."""
        quiz = Quiz.objects.create(title='Quiz')
        q = Question.objects.create(
            quiz=quiz,
            text='To delete',
            options='["A","B"]',
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        url = reverse('question_detail', kwargs={'question_id': q.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Question.objects.filter(pk=q.id).exists()
