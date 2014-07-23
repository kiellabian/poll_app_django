from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Poll, Choice

# def index(request):
# 	latest_polls = Poll.objects.order_by('-pub_date')[:5]
# 	context = {'latest_polls': latest_polls}
# 	return render(request, 'polls/index.html', context)

# def details(request, poll_id):
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	context = {'poll': poll}
# 	return render(request, 'polls/details.html', context)

# def results(request, poll_id):
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	context = {'poll': poll}
# 	return render(request, 'polls/results.html', context)

def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		context = {'poll': poll, 'error_message': 'ERROR!'}
		return render(request, 'polls/details.html', context)
	else:
		choice.vote_count += 1
		choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_polls'

	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/details.html'

	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now())