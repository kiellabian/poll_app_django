import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from polls.models import Poll

class PollViewTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		"""
		A future poll should not be considered as published recently.
		"""
		future_poll = Poll(pub_date=timezone.now()+datetime.timedelta(days=7))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_old_poll(self):
		"""
		A poll older than 1 day should not be considered as published recently.
		"""
		future_poll = Poll(pub_date=timezone.now()-datetime.timedelta(days=7))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_recent_poll(self):
		"""
		A recently published poll by an hour should be considered recent.
		"""
		future_poll = Poll(pub_date=timezone.now()-datetime.timedelta(hours=1))
		self.assertEqual(future_poll.was_published_recently(), True)

def create_poll(question, days):
	return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollIndexViewTests(TestCase):

	def test_index_view_with_no_polls(self):
		"""
		If no polls exist, a message should be shown.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No latest poll")
		self.assertQuerysetEqual(response.context['latest_polls'], [])

	def test_index_view_with_past_poll(self):
		"""
		A poll in the past should be shown in the index page
		"""
		create_poll(question='past poll', days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_polls'], ['<Poll: past poll>'])

	def test_index_view_with_future_poll(self):
		"""
		A poll in the future should not be shown in the index page
		"""
		create_poll(question='future poll', days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No latest poll", status_code=200)
		self.assertQuerysetEqual(response.context['latest_polls'], [])

	def test_index_view_with_future_and_past_poll(self):
		"""
		A poll in the future should not be shown in the index page
		A poll in the past should be shown in the index page
		"""
		create_poll(question='future poll', days=30)
		create_poll(question='past poll', days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_polls'], ['<Poll: past poll>'])

	def test_index_view_with_two_past_polls(self):
		"""
		The two polls should be shown in the index page
		"""
		create_poll(question='past poll 1', days=-30)
		create_poll(question='past poll 2', days=-7)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_polls'], ['<Poll: past poll 2>', '<Poll: past poll 1>'])

class PollDetailTests(TestCase):

	# def test_detail_view_with_future_poll(self):
	# 	"""
	# 	A detail view should show 404 Error page for a future poll
	# 	"""
	# 	poll = create_poll(question='future poll', days=7)
	# 	response = self.client.get(reverse('polls:index'), args=(poll.id,))
	# 	self.assertEqual(response.status_code, 404)

	def test_detail_view_with_past_poll(self):
		"""
		A detail view should show the page for a past poll
		"""
		poll = create_poll(question='past poll', days=-7)
		response = self.client.get(reverse('polls:index'), args=(poll.id,))
		self.assertContains(response, poll.question, status_code=200)