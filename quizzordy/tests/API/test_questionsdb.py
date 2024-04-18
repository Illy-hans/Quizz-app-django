from django.test import TestCase, Client
from quizzordy.models import QuestionsDB 
from unittest.mock import patch
from django.http import JsonResponse

class AddViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('quizzordy.views.requests.get')
    def test_add_success(self, mock_get):
        # Mocking the requests.get method to return a sample response
        mock_get.return_value.status_code = 201
        mock_get.return_value.json.return_value = {
            'results': [
                {
                    'category': 'Test Category',
                    'question': 'Test Question',
                    'correct_answer': 'Test Correct Answer',
                    'incorrect_answers': ['Test Incorrect Answer']
                }
            ]
        }

        # Making a GET request to the add view
        response = self.client.get('/questionsdb/add')

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 201)

        # Check if the QuestionsDB object is created with the correct data
        self.assertTrue(QuestionsDB.objects.filter(
            category='Test Category',
            question='Test Question',
            correct_answer='Test Correct Answer',
            incorrect_answers=['Test Incorrect Answer']
        ).exists())

    @patch('quizzordy.views.requests.get')
    def test_add_failure(self, mock_get):
        # Mocking the requests.get method to return a failed response
        mock_get.return_value.status_code = 500

        # Making a GET request to the add view
        response = self.client.get('/questionsdb/add')

        # Check if the response status code is 500
        self.assertEqual(response.status_code, 500)

        # Check if the error message is present in the response
        self.assertTrue(JsonResponse({"error": "Failed to fetch data from the external API"}, status=500).content in response.content)
