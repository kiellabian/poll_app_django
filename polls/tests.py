import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from polls.models import Poll

class PollMethodTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		"""Test for Poll pub_date"""
		future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=1), question="YOLO?")
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_past_poll(self):
		"""Test for Poll pub_date"""
		future_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=2), question="YOLO?")
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_present_poll(self):
		"""Test for Poll pub_date"""
		future_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1), question="YOLO?")
		self.assertEqual(future_poll.was_published_recently(), True)

def create_poll(question, days):
	return Poll(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):

	def test_index_view_with_future_and_past_polls(self):
		"""Test index page, future poll must not show, past poll might show"""
		create_poll(question="future poll", days=30).save()
		create_poll(question="past poll", days=-30).save()
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], ['<Poll: past poll>']
		)