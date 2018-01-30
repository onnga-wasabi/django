from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, qustion_id):
    return HttpResponse("You're lookin at quesion %s." % question_id)


def results(request, qustion_id):
    response = "You're looking at the results of question %s." % question_id)
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
