import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def register(request):
  form = UserCreationForm()

  if request.method == "POST":
      form = UserCreationForm(request.POST)
      if form.is_valid():
          form.save()
          messages.success(request, 'Your account has been successfully created')
          return redirect('authentication:login')
  
  context = {'form':form}
  return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user) # melakukan login terlebih dahulu
          response = HttpResponseRedirect(reverse("homepage:show_homepage")) # membuat response
          response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
          return response
      else:
          messages.info(request, 'Username atau Password salah!')
  context = {}
  return render(request, 'login.html', context)

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response