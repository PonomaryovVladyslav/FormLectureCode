from django.urls import path

from .views import form_view, employee, fail, congrats, my_login, my_logout, my_register, change_pass, comments_view

urlpatterns = [
    path('form-url/', form_view, name='form-view'),
    path('', employee, name='employee'),
    path('fail/', fail, name='fail'),
    path('congrats/', congrats, name='congrats'),
    path('login/', my_login, name='login'),
    path('logout/', my_logout, name='logout'),
    path('register/', my_register, name='register'),
    path('change-pass/', change_pass, name='change-pass'),
    path('comments/', comments_view, name='comments'),
]
