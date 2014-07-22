from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from polls.models import Poll

# class DetailView(generic.DetailView):
# 	model = Poll
# 	template_name = 'polls/detail.html'

def index(request):
	latest_polls = Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
	context = {'latest_polls': latest_polls}
	return render(request, 'polls/index.html', context)

def detail(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	if poll.pub_date > timezone.now():
		raise Http404
	else:
		context = {'poll': poll}
		return render(request, 'polls/detail.html', context)

def results(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	context = {'poll': poll}
	return render(request, 'polls/result.html', context)

def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		context = {'poll':poll, 'error_message':'You didn\'t choose anything!'}
		return render(request, 'poll/detail.html', context)
	else:
		choice.votes += 1
		choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(poll_id)))