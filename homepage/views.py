import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse
from homepage.forms import FeedbackForm
from django.urls import reverse
from homepage.forms import FeedbackForm
from homepage.models import Feedback
from django.core import serializers

# Create your views here.
@login_required(login_url='/authentication/login/')
def show_homepage(request):
    form = FeedbackForm()
    context = {
        'name': request.user.username,
        'class': 'PBP B',
        'last_login': request.COOKIES['last_login'],
        # 'last_feedback': request.session.get('last_feedback', 'Belum ada feedback yang diberikan'),
        'form':form,
    }

    return render(request, "homepage.html", context)


@login_required(login_url='/authentication/login/')
def submit_feedback(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return HttpResponseRedirect(reverse('homepage:show_homepage'))
        # response = serializers.serialize('json',[new_feedback])
        # request.session['last_feedback'] = str(datetime.datetime.now())
    return HttpResponseBadRequest


def show_json(request):
    data = Feedback.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")