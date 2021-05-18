from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django.http import Http404

from polls.models import Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question_obj = get_object_or_404(Question, id=question_id)
    # try:
    #     question_obj = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return render(request, 'polls/detail.html', {'question': question_obj})


def results(request, question_id):
    response = "You'r looking at the result of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You'r voting on question %s." % question_id)