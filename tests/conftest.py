import pytest
import json
from quiz.services.category import CategoryService
from quiz.services.quiz import QuizService
from quiz.services.question import QuestionService
from quiz.models import Difficulty, Quiz

@pytest.fixture
def category_service():
    return CategoryService()

@pytest.fixture
def quiz_service():
    return QuizService()

@pytest.fixture
def question_service():
    return QuestionService()

@pytest.fixture
def category(category_service):
    return category_service.create_category('Default Category')

@pytest.fixture
def quiz(quiz_service):
    return quiz_service.create_quiz({'title': 'Default Quiz', 'description': 'Default Desc'})

@pytest.fixture
def question(question_service, quiz):
    data = {
        'quiz_id': quiz.id,
        'text': 'Default question?',
        'options': json.dumps(['A', 'B', 'C']),
        'correct_answer': 'A',
        'difficulty': Difficulty.EASY,
    }
    return question_service.create_question(quiz.id, data)
