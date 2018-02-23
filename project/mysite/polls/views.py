from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    # いままで通り表示するviewを指定する
    template_name = 'polls/index.html'
    # renderと共に渡していたcontextの変数名
    # defaultの場合は(おそらくmodel=Questionとかやってれば)question_listになる
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # この関数を定義してやると上で指定したcontext_object_nameに渡されるっぽい
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # defaultの場合context_object_nameはquestionになる
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question.objects.filter(
        pub_date__lte=timezone.now()), pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # リダイレクトreverseはurls.py
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
