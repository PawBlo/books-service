from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('secured/', secured_view, name='secured'),
    path('logout/', logout, name="logout"),
    path('change_password/', change_password, name = "change-password")

]