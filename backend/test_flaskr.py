import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()




class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.database_host = os.getenv("DATABASE_HOST")
        self.test_database_name = os.getenv("TEST_DATABASE_NAME")
        self.database_path = 'postgresql://{}/{}'.format(self.database_host, self.test_database_name)
    
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })
        setup_db(self.app, self.database_path)

        self.client = self.app.test_client

        self.new_question = {"question":"What is the capital of France", "answer":"Paris", "category":"5", "difficulty":"2"}
    
    def tearDown(self):
        """Executed after reach test"""
    pass
    # Tests
    #  
    def test_get_paignated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))


    def test_404_request_beyond_valid_pages(self):
        res = self.client().get('/questions?page=2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_category(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_add_question(self):
        response = self.client().post('/questions', json=self.new_question)
        self.assertTrue(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_delete_question(self):
        response = self.client().delete('/questions/11')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 11)


    def test_422_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request Cannot Be Processed')
    
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'one'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_retrieve_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': '5', 'type': 'Entertainment'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 5)

    def test_422_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request Cannot Be Processed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()