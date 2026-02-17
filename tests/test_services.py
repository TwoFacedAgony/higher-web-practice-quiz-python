"""Тесты для сервисов приложения quiz."""

import json
import pytest
from django.http import Http404

from quiz.models import Difficulty, Quiz
from quiz.services.category import CategoryService
from quiz.services.quiz import QuizService
from quiz.services.question import QuestionService


@pytest.mark.django_db
class TestCategoryService:
    """Тесты сервиса категорий."""

    def test_create_and_get_category(self, category_service):
        """Тестирует создание категории и получение её по идентификатору."""
        title_example = 'Programming'
        category = category_service.create_category(title_example)
        fetched = category_service.get_category(category.id)
        assert fetched is not None
        assert fetched.title == title_example

    def test_update_category(self, category_service, category):
        """Тестирует обновление существующей категории."""
        updated = category_service.update_category(
            category.id,
            {'title': 'Update'}
        )
        assert updated is not None
        assert updated.title == 'Update'

        category_from_db = category_service.get_category(category.id)
        assert category_from_db.title == 'Update'

    def test_delete_category(self, category_service, category):
        """Тестирует удаление категории."""
        initial_count = len(category_service.list_categories())
        cat_id = category.id
        category_service.delete_category(cat_id)
        assert len(category_service.list_categories()) == initial_count - 1
        # Проверяем, что get_category теперь вызывает Http404
        with pytest.raises(Http404):
            category_service.get_category(cat_id)

    def test_list_categories(self, category_service):
        """Тестирует получение списка всех категорий."""
        cat_a = category_service.create_category('A')
        cat_b = category_service.create_category('B')
        categories = category_service.list_categories()
        titles = [c.title for c in categories]
        assert cat_a.title in titles
        assert cat_b.title in titles

    def test_get_category_returns_none_for_missing_id(self, category_service):
        """Тестирует, что get_category вызывает Http404 для несуществующего ID."""
        with pytest.raises(Http404):
            category_service.get_category(99999)

    def test_update_category_returns_none_for_missing_id(self, category_service):
        """Тестирует, что update_category вызывает Http404 для несуществующего ID."""
        with pytest.raises(Http404):
            category_service.update_category(99999, {'title': 'Example'})


@pytest.mark.django_db
class TestQuizService:
    """Тесты сервиса квизов."""

    def test_create_and_get_quiz(self, quiz_service):
        """Тестирует создание квиза и получение его по идентификатору."""
        title = 'Arithmetics'
        description = 'Numbers'
        quiz = quiz_service.create_quiz({'title': title, 'description': description})
        fetched = quiz_service.get_quiz(quiz.id)
        assert fetched is not None
        assert fetched.title == title
        assert fetched.description == description

    def test_list_quizzes(self, quiz_service):
        """Тестирует получение списка всех квизов."""
        quiz_a = quiz_service.create_quiz({'title': 'Quiz A'})
        quiz_b = quiz_service.create_quiz({'title': 'Quiz B'})
        quizzes = quiz_service.list_quizzes()
        titles = [q.title for q in quizzes]
        assert quiz_a.title in titles
        assert quiz_b.title in titles

    def test_get_quiz_returns_none_for_missing_id(self, quiz_service):
        """Тестирует, что get_quiz вызывает Http404 для несуществующего ID."""
        with pytest.raises(Http404):
            quiz_service.get_quiz(99999)

    def test_get_quizzes_by_title(self, quiz_service):
        """Тестирует поиск квизов по части названия."""
        py_basics = quiz_service.create_quiz({'title': 'Python Basics'})
        py_advanced = quiz_service.create_quiz({'title': 'Python Advanced'})
        java_intro = quiz_service.create_quiz({'title': 'Java Intro'})

        result = quiz_service.get_quizes_by_title('Python')
        result_ids = [q.id for q in result]
        assert py_basics.id in result_ids
        assert py_advanced.id in result_ids
        assert java_intro.id not in result_ids

    def test_update_quiz(self, quiz_service, quiz):
        """Тестирует обновление существующего квиза."""
        updated = quiz_service.update_quiz(
            quiz.id,
            {'title': 'New', 'description': 'New desc'}
        )
        assert updated is not None
        assert updated.title == 'New'
        assert updated.description == 'New desc'

        quiz_from_db = quiz_service.get_quiz(quiz.id)
        assert quiz_from_db.title == 'New'
        assert quiz_from_db.description == 'New desc'

    def test_update_quiz_returns_none_for_missing_id(self, quiz_service):
        """Тестирует, что update_quiz вызывает Http404 для несуществующего ID."""
        with pytest.raises(Http404):
            quiz_service.update_quiz(99999, {'title': 'New'})

    def test_delete_quiz(self, quiz_service, quiz):
        """Тестирует удаление квиза."""
        qid = quiz.id
        quiz_service.delete_quiz(qid)
        # Проверяем, что get_quiz теперь вызывает Http404
        with pytest.raises(Http404):
            quiz_service.get_quiz(qid)


@pytest.mark.django_db
class TestQuestionService:
    """Тесты сервиса вопросов."""

    def _question_data(self, quiz_id, **overrides):
        """Базовые данные для создания вопроса."""
        data = {
            'quiz_id': quiz_id,
            'text': 'What is 2+2?',
            'options': json.dumps(['3', '4', '5']),
            'correct_answer': '4',
            'difficulty': Difficulty.EASY,
        }
        data.update(overrides)
        return data

    def test_create_and_get_question(self, question_service, quiz):
        """Тестирует создание вопроса и получение его по идентификатору."""
        text = 'Capital of France?'
        data = {
            'text': text,
            'options': json.dumps(['London', 'Paris', 'Berlin']),
            'correct_answer': 'Paris',
            'difficulty': Difficulty.EASY,
        }
        question = question_service.create_question(quiz.id, data)
        fetched = question_service.get_question(question.id)
        assert fetched is not None
        assert fetched.text == text
        assert fetched.correct_answer == 'Paris'

    def test_list_questions(self, question_service, quiz):
        """Тестирует получение списка всех вопросов."""
        q1 = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='Q1')
        )
        q2 = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='Q2')
        )
        questions = question_service.list_questions()
        question_ids = [q.id for q in questions]
        assert q1.id in question_ids
        assert q2.id in question_ids

    def test_get_question_returns_none_for_missing_id(self, question_service):
        """Тестирует, что get_question вызывает Http404 для несуществующего ID."""
        with pytest.raises(Http404):
            question_service.get_question(99999)

    def test_get_questions_by_text(self, question_service, quiz):
        """Тестирует поиск вопросов по части текста."""
        unique_text = 'Unique searchable phrase here'
        q = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text=unique_text),
        )
        result = question_service.get_questions_by_text('searchable')
        result_ids = [r.id for r in result]
        assert q.id in result_ids

    def test_get_questions_for_quiz(self, question_service, quiz):
        """Тестирует получение всех вопросов для указанного квиза."""
        other_quiz = Quiz.objects.create(title='Other')
        q1 = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='In first')
        )
        q2 = question_service.create_question(
            other_quiz.id,
            self._question_data(other_quiz.id, text='In other')
        )
        questions = question_service.get_questions_for_quiz(quiz.id)
        assert len(questions) == 1
        assert questions[0].id == q1.id

    def test_update_question(self, question_service, quiz):
        """Тестирует обновление существующего вопроса."""
        question = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='Original'),
        )
        updated = question_service.update_question(
            question.id,
            {'text': 'Updated text'}
        )
        assert updated is not None
        assert updated.text == 'Updated text'

        question_from_db = question_service.get_question(question.id)
        assert question_from_db.text == 'Updated text'

    def test_update_question_returns_none_for_missing_id(self, question_service):
        """Тестирует, что update_question вызывает Http404 для несуществующего ID."""
        with pytest.raises(Http404):
            question_service.update_question(99999, {'text': 'X'})

    def test_delete_question(self, question_service, quiz):
        """Тестирует удаление вопроса."""
        question = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='To delete'),
        )
        qid = question.id
        question_service.delete_question(qid)
        # Проверяем, что get_question теперь вызывает Http404
        with pytest.raises(Http404):
            question_service.get_question(qid)

    @pytest.mark.parametrize(
        'right_answer',
        ('42', ' 42 ')
    )
    def test_check_answer_correct(self, right_answer, question_service, quiz):
        """Тестирует проверку правильного ответа (с учётом пробелов)."""
        question = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, correct_answer=right_answer),
        )
        assert question_service.check_answer(question.id, right_answer) is True

    def test_check_answer_incorrect(self, question_service, quiz):
        """Тестирует проверку неправильного ответа."""
        question = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, correct_answer='42'),
        )
        assert question_service.check_answer(question.id, '0') is False
        assert question_service.check_answer(question.id, '') is False

    def test_check_answer_returns_false_for_missing_question(self, question_service):
        """Тестирует, что check_answer вызывает Http404 для несуществующего вопроса."""
        with pytest.raises(Http404):
            question_service.check_answer(99999, 'any')

    def test_random_question_from_quiz(self, question_service, quiz):
        """Тестирует получение случайного вопроса из квиза."""
        q1 = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='Q1')
        )
        q2 = question_service.create_question(
            quiz.id,
            self._question_data(quiz.id, text='Q2')
        )
        question = question_service.random_question_from_quiz(quiz.id)
        assert question is not None
        assert question.quiz_id == quiz.id
        assert question.id in (q1.id, q2.id)

    def test_random_question_from_quiz_raises_when_empty(self, question_service):
        """Тестирует, что метод выбрасывает ValueError, если в квизе нет вопросов."""
        empty_quiz = Quiz.objects.create(title='Empty Quiz')
        with pytest.raises(ValueError, match='No questions found'):
            question_service.random_question_from_quiz(empty_quiz.id)
