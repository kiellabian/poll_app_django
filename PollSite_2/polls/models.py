import datetime
from django.db import models
from django.utils import timezone

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __unicode__(self):
		return self.question

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.short_description = "Recently Published?"
	was_published_recently.boolean = True

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.text