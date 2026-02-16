"""Тесты для сервисов приложения quiz."""

import json
import pytest

from quiz.models import Category, Quiz, Difficulty
from quiz.services.category import CategoryService
from quiz.services.quiz import QuizService
from quiz.services.question import QuestionService


@pytest.mark.django_db
class TestCategoryService:
    """Тесты сервиса категорий."""

    def setup_method(self) -> None:
        """Подготавливает сервис категорий перед каждым тестом."""
        self.service = CategoryService()

    def test_create_and_get_category(self) -> None:
        """Тестирует создание категории и получение её по идентификатору."""
        category = self.service.create_category('Programming')
        fetched = self.service.get_category(category.id)
        assert fetched is not None
        assert fetched.title == 'Programming'

    def test_update_category(self) -> None:
        """Тестирует обновление существующей категории."""
        category = Category.objects.create(title='Example')
        updated = self.service.update_category(
            category.id,
            {'title': 'Update'}
        )
        assert updated is not None
        assert updated.title == 'Update'

    def test_delete_category(self) -> None:
        """Тестирует удаление категории."""
        category = Category.objects.create(title='Temp')
        self.service.delete_category(category.id)
        assert Category.objects.count() == 0

    def test_list_categories(self) -> None:
        """Тестирует получение списка всех категорий."""
        Category.objects.create(title='A')
        Category.objects.create(title='B')
        categories = self.service.list_categories()
        assert len(categories) == 2
        titles = [c.title for c in categories]
        assert 'A' in titles and 'B' in titles

    def test_get_category_returns_none_for_missing_id(self) -> None:
        """
        Тестирует, что get_category возвращает None для несуществующего ID.
        """
        result = self.service.get_category(99999)
        assert result is None

    def test_update_category_returns_none_for_missing_id(self) -> None:
        """
        Тестирует, что update_category возвращает None для несуществующего ID.
        """
        result = self.service.update_category(
            99999,
            {'title': 'Example'}
        )
        assert result is None


@pytest.mark.django_db
class TestQuizService:
    """Тесты сервиса квизов."""

    def setup_method(self) -> None:
        """Подготавливает сервис квизов перед каждым тестом."""
        self.service = QuizService()

    def test_create_and_get_quiz(self) -> None:
        """Тестирует создание квиза и получение его по идентификатору."""
        quiz = self.service.create_quiz(
            {'title': 'Ariphmetics', 'description': 'Numbers'}
        )
        fetched = self.service.get_quiz(quiz.id)
        assert fetched is not None
        assert fetched.title == 'Ariphmetics'
        assert fetched.description == 'Numbers'

    def test_list_quizzes(self) -> None:
        """Тестирует получение списка всех квизов."""
        self.service.create_quiz({'title': 'Quiz A'})
        self.service.create_quiz({'title': 'Quiz B'})
        quizzes = self.service.list_quizzes()
        assert len(quizzes) == 2

    def test_get_quiz_returns_none_for_missing_id(self) -> None:
        """Тестирует, что get_quiz возвращает None для несуществующего ID."""
        assert self.service.get_quiz(99999) is None

    def test_get_quizes_by_title(self) -> None:
        """Тестирует поиск квизов по части названия."""
        self.service.create_quiz({'title': 'Python Basics'})
        self.service.create_quiz({'title': 'Python Advanced'})
        self.service.create_quiz({'title': 'Java Intro'})
        result = self.service.get_quizes_by_title('Python')
        assert len(result) == 2
        titles = [q.title for q in result]
        assert 'Python Basics' in titles and 'Python Advanced' in titles

    def test_update_quiz(self) -> None:
        """Тестирует обновление существующего квиза."""
        quiz = Quiz.objects.create(title='Old', description='Desc')
        updated = self.service.update_quiz(
            quiz.id,
            {'title': 'New', 'description': 'New desc'}
        )
        assert updated is not None
        assert updated.title == 'New'
        assert updated.description == 'New desc'

    def test_update_quiz_returns_none_for_missing_id(self) -> None:
        """
        Тестирует, что update_quiz возвращает None для несуществующего ID.
        """
        assert self.service.update_quiz(99999, {'title': 'New'}) is None

    def test_delete_quiz(self) -> None:
        """Тестирует удаление квиза."""
        quiz = Quiz.objects.create(title='To Delete')
        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.filter(pk=quiz.id).count() == 0


def _question_data(quiz_id: int, **overrides) -> dict:
    """
    Возвращает минимальный набор данных для создания вопроса.

    :param quiz_id: Идентификатор квиза, к которому относится вопрос.
    :param overrides: Дополнительные поля для переопределения стандартных.
    :return: Словарь с данными вопроса.
    """
    data = {
        'quiz_id': quiz_id,
        'text': 'What is 2+2?',
        'options': json.dumps(['3', '4', '5']),
        'correct_answer': '4',
        'difficulty': Difficulty.EASY,
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
class TestQuestionService:
    """Тесты сервиса вопросов."""

    def setup_method(self) -> None:
        """Подготавливает сервис вопросов и создаёт тестовый квиз."""
        self.service = QuestionService()
        self.quiz = Quiz.objects.create(title='Test Quiz')

    def test_create_and_get_question(self) -> None:
        """Тестирует создание вопроса и получение его по идентификатору."""
        data = {
            'text': 'Capital of France?',
            'options': json.dumps(['London', 'Paris', 'Berlin']),
            'correct_answer': 'Paris',
            'difficulty': Difficulty.EASY,
        }
        question = self.service.create_question(self.quiz.id, data)
        fetched = self.service.get_question(question.id)
        assert fetched is not None
        assert fetched.text == 'Capital of France?'
        assert fetched.correct_answer == 'Paris'

    def test_list_questions(self) -> None:
        """Тестирует получение списка всех вопросов."""
        self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='Q1')
        )
        self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='Q2')
        )
        questions = self.service.list_questions()
        assert len(questions) >= 2

    def test_get_question_returns_none_for_missing_id(self) -> None:
        """
        Тестирует, что get_question возвращает None для несуществующего ID.
        """
        assert self.service.get_question(99999) is None

    def test_get_questions_by_text(self) -> None:
        """Тестирует поиск вопросов по части текста."""
        self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='Unique searchable phrase here'),
        )
        result = self.service.get_questions_by_text('searchable')
        assert len(result) >= 1
        assert any('searchable' in q.text for q in result)

    def test_get_questions_for_quiz(self) -> None:
        """Тестирует получение всех вопросов для указанного квиза."""
        other_quiz = Quiz.objects.create(title='Other')
        self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='In first')
        )
        self.service.create_question(
            other_quiz.id,
            _question_data(other_quiz.id, text='In other')
        )
        questions = self.service.get_questions_for_quiz(self.quiz.id)
        assert len(questions) == 1
        assert questions[0].text == 'In first'

    def test_update_question(self) -> None:
        """Тестирует обновление существующего вопроса."""
        question = self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='Original'),
        )
        updated = self.service.update_question(
            question.id,
            {'text': 'Updated text'}
        )
        assert updated is not None
        assert updated.text == 'Updated text'

    def test_update_question_returns_none_for_missing_id(self) -> None:
        """
        Тестирует, что update_question возвращает None для несуществующего ID.
        """
        assert self.service.update_question(99999, {'text': 'X'}) is None

    def test_delete_question(self) -> None:
        """Тестирует удаление вопроса."""
        question = self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='To delete'),
        )
        self.service.delete_question(question.id)
        assert self.service.get_question(question.id) is None

    def test_check_answer_correct(self) -> None:
        """Тестирует проверку правильного ответа (с учётом пробелов)."""
        question = self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, correct_answer='42'),
        )
        assert self.service.check_answer(question.id, '42') is True
        assert self.service.check_answer(question.id, ' 42 ') is True

    def test_check_answer_incorrect(self) -> None:
        """Тестирует проверку неправильного ответа."""
        question = self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, correct_answer='42'),
        )
        assert self.service.check_answer(question.id, '0') is False
        assert self.service.check_answer(question.id, '') is False

    def test_check_answer_returns_false_for_missing_question(self) -> None:
        """
        Тестирует, что check_answer возвращает False для
        несуществующего вопроса.
        """
        assert self.service.check_answer(99999, 'any') is False

    def test_random_question_from_quiz(self) -> None:
        """Тестирует получение случайного вопроса из квиза."""
        self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='Q1')
        )
        self.service.create_question(
            self.quiz.id,
            _question_data(self.quiz.id, text='Q2')
        )
        question = self.service.random_question_from_quiz(self.quiz.id)
        assert question is not None
        assert question.quiz_id == self.quiz.id
        assert question.text in ('Q1', 'Q2')

    def test_random_question_from_quiz_raises_when_empty(self) -> None:
        """
        Тестирует, что метод выбрасывает ValueError, если в квизе нет вопросов.
        """
        empty_quiz = Quiz.objects.create(title='Empty Quiz')
        with pytest.raises(ValueError, match='No questions found'):
            self.service.random_question_from_quiz(empty_quiz.id)
