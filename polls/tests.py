import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from polls.models import Poll

def create_poll(question, days):
	return Poll(question = question, pub_date = timezone.now()+datetime.timedelta(days=days))

class PollModelTests(TestCase):
	
	def test_was_published_recently_method_with_future_poll(self):
		"""
		A future poll is not published recently
		"""
		future_poll = create_poll('future poll', 7)
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_method_with_past_poll(self):
		"""
		A past poll (7 days old) is not published recently
		"""
		past_poll = create_poll('past poll', -7)
		self.assertEqual(past_poll.was_published_recently(), False)

	def test_was_published_recently_method_with_new_poll(self):
		"""
		A new poll is published recently
		"""
		new_poll = create_poll('new poll', 0)
		self.assertEqual(new_poll.was_published_recently(), True)

class PollIndexViewTests(TestCase):

	def test_index_view_with_no_polls(self):
		"""
		Index view should contain no polls
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_polls'], [])

	def test_index_view_with_past_and_future_poll(self):
		"""
		Index view should contain the past poll but not the future poll
		"""
		create_poll('past poll', -7).save()
		create_poll('future poll', 7).save()
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_polls'], ['<Poll: past poll>'])

	def test_index_view_with_past_and_new_poll(self):
		"""
		Index view should contain both past and new poll at the right order
		"""
		create_poll('new poll', 0).save()
		create_poll('past poll', -7).save()
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_polls'], ['<Poll: new poll>', '<Poll: past poll>'])

class PollDetailViewTests(TestCase):

	def test_detail_view_with_future_poll(self):
		"""
		Detail View should raise 404 for future poll
		"""
		future_poll = create_poll('future poll', 7)
		future_poll.save()
		response = self.client.get(reverse('polls:details', args=(future_poll.id, )))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_past_poll(self):
		"""
		Detail View should be fine with a past poll
		"""
		past_poll = create_poll('past poll', -7)
		past_poll.save()
		response = self.client.get(reverse('polls:details', args=(past_poll.id, )))
		self.assertContains(response, past_poll.question, status_code=200)
