from django.http import response
from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse

def create_question(question_text, days):
    """
    Create a question with given 'question_text' 
    and pubished the given number of 'days' offset to now.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTest(TestCase):

    def test_was_published_recently_whit_future_question(self):
        time = timezone.now() + datetime.timedelta(30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_wit_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QustionIndexViewTests(TestCase):

    url = reverse('polls:index')
    def test_no_question(self):
        """
        if no question exist, an appropriate message is displayed.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with 'pub_date' in the past are displayed on the index page.
        """
        past_qustion = create_question(question_text='past question', days=-30)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_qustion]
        )

    def test_future_question(self):
        """
        Question with a 'pub_date' on the future aren't displayed on th index page.
        """
        future_question = create_question("Future question", 30)
        response = self.client.get(self.url)
        self.assertContains(response, 'No polls')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question("Future question", 2)
        past_question = create_question("past question", -2)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )
    
    def test_two_past_question(self):
        question1 = create_question("past question 1", -30)
        question2 = create_question('past question 2', -2)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text="future question", days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the detail view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question('Past question', -30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, "Past question")


class QuestionResultViewTest(TestCase):

    def test_future_question(self):
        """
        the result view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question("futuer question", 30)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the result view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question("past question", -30)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(
            response.context['question'],
            past_question
        )
        self.assertContains(response, "past question")
    
