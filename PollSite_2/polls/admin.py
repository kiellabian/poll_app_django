from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
	"""docstring for ChoiceInline"""
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	"""docstring for PollAdmin"""
	fieldsets= [
		(None, {'fields': ['question']}),
		("Dates", {'fields': ['pub_date']})
	]
	inlines = [ChoiceInline]
	list_display = ('id', 'question', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question', 'pub_date']

admin.site.register(Poll, PollAdmin)
