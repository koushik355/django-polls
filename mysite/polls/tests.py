import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

from .models import Question


def create_question(question_text, days):
    """
    Create a question
    :param question_text:
    :param days:
    :return: Question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns false for question with future publish date
        :return:
        :rtype:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for question that was published
        the last day
        :return:
        """
        last_day = now() - datetime.timedelta(hours=23)
        question = Question(pub_date=last_day)
        self.assertIs(question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    no_poll_msg = "No polls are available"

    def test_no_question(self):
        """
        If no question exists, an appropriate msg is displayed
        :return:
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.no_poll_msg)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Question with past date is displayed on the index page
        :return:
        """
        create_question('Past question', -3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_future_question(self):
        """
        Question with future date is not displayed on the index page
        :return:
        """
        create_question('Future Question', 3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response, self.no_poll_msg)

    def test_question_with_no_choice(self):
        """
        Question with no choice should not be displayed on the index page
        :return:
        """
        create_question('No choice question', -3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response, self.no_poll_msg)


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        question = create_question('Future question', 3)
        response = self.client.get(reverse('polls:detail', args=[question.id, ]))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        question = create_question('Past question', -3)
        response = self.client.get(reverse('polls:detail', args=[question.id, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
