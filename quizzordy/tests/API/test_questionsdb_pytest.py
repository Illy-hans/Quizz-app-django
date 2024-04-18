from unittest.mock import patch
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from ...models import QuestionsDB

@pytest.mark.django_db
class TestAddView:
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
        client = APIClient()
        response = client.get('/questionsdb/add')

        # Check if the response status code is 201
        assert response.status_code == status.HTTP_201_CREATED

        # Check if the QuestionsDB object is created with the correct data
        assert QuestionsDB.objects.filter(
            category='Test Category',
            question='Test Question',
            correct_answer='Test Correct Answer',
            incorrect_answers=['Test Incorrect Answer']
        ).exists()

    @patch('quizzordy.views.requests.get')
    def test_add_failure(self, mock_get):
        # Mocking the requests.get method to return a failed response
        mock_get.return_value.status_code = 500

        # Making a GET request to the add view
        client = APIClient()
        response = client.get('/questionsdb/add')

        # Check if the response status code is 500
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        # Check if the error message is present in the response
        assert b'{"error":"Failed to fetch data from the external API"}' in response.content