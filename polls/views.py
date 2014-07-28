from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Poll, Choice

# def index(request):
# 	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
# 	context = {'latest_poll_list': latest_poll_list}
# 	return render(request, 'polls/index.html', context)

# def details(request, poll_id):
# 	poll = get_object_or_404(Poll, id=poll_id)
# 	return render(request, 'polls/detail.html', {'poll': poll})

# def results(request, poll_id):
# 	poll = get_object_or_404(Poll, id=poll_id)
# 	return render(request, 'polls/result.html', {'poll': poll})

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		""""Return latest 5 polls"""
		return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
		
class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/result.html'

def vote(request, poll_id):
	poll = get_object_or_404(Poll, id=poll_id)

	try:
		choice = poll.choice_set.get(id=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {'poll':poll, 'error_message':"No choice was selected."})
	else:
		choice.votes += 1
		choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))

