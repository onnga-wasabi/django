from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = Question(
            pub_date=timezone.now() + datetime.timedelta(days=1))
        self.assertIs(future_question.was_published_recently(), False)
