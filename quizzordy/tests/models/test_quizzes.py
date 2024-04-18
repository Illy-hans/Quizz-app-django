from django.test import TestCase 
from quizzordy.models import Quizzes
from django.contrib.auth.models import User
from datetime import datetime, timezone

class Test_Quizzes(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(first_name="Ikram", last_name="Ibrahim", email="miss_missy@gmail.com",
                                            password="12345")
        self.test_model = Quizzes.objects.create(score="0.8", user=self.test_user)

    def tearDown(self):
        self.test_model.delete()
        self.test_user.delete()
    
    def test_quizz_saved(self):

        saved_quizz = Quizzes.objects.get(id=self.test_model.id)
        test_timestamp = datetime.now(timezone.utc).replace(microsecond=0)

        self.assertEqual(saved_quizz.timestamp.replace(microsecond=0), test_timestamp)
        self.assertEqual(saved_quizz.score, 0.8)
        self.assertEqual(saved_quizz.user, self.test_user)



