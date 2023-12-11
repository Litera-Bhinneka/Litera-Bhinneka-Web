from django.urls import path
from auth_flutter.views import login, logout, register

app_name = 'auth_flutter'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]