from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days):
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = Question(
            pub_date=timezone.now() + datetime.timedelta(days=1))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        future_question = Question(
            pub_date=timezone.now() - datetime.timedelta(days=1, seconds=1))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        future_question = Question(
            pub_date=timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59))
        self.assertIs(future_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    '''
    questionがない時
    過去のquestion
    過去と未来のquestion
    未来のquestion
    過去のquestionが正しくソートされるかどうか
    '''

    def test_no_quesions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_quesions(self):
        create_question('past question.', days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: past question.>'])

    def test_future_quesions(self):
        create_question('future question.', days=3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_quesions(self):
        create_question('future question.', days=3)
        create_question('past question.', days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: past question.>'])

    def test_two_past_quesions(self):
        create_question('past1 question.', days=-5)
        create_question('past2 question.', days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
            '<Question: past2 question.>', '<Question: past1 question.>'])


class DetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question('future question', days=3)
        response = self.client.get(
            reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question('past question', days=-3)
        response = self.client.get(
            reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)


class ResultsViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question('future question', days=3)
        response = self.client.get(
            reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question('past question', days=-3)
        response = self.client.get(
            reverse('polls:results', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)


class VoteViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question('future question', days=3)
        response = self.client.get(
            reverse('polls:vote', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question('past question', days=-3)
        response = self.client.get(
            reverse('polls:vote', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
