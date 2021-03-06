from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            choice__id__isnull=False
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        error_msg = 'You did not select a choice'
        return render(request, 'polls/detail.html', {'question': question, 'error_msg': error_msg})
    else:
        choice.vote += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))


def testing(request):
    text = f"""
            questions: {Question.objects.all()}
        """
    return HttpResponse(text, content_type='text/plain')
