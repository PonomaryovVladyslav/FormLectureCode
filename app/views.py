from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from app.forms import MyForm, EmployeeForm, AuthenticationForm, RegistrationForm, ChangePassForm, CommentFilterForm
from app.models import Comment


class MyClass:
    string = ''

    def __init__(self, s):
        self.string = s


def index(request):
    my_num = 33
    my_str = 'some string'
    my_dict = {"some_key": "some_value"}
    my_list = ['list_first_item', 'list_second_item', 'list_third_item']
    my_set = {'set_first_item', 'set_second_item', 'set_third_item'}
    my_tuple = ('tuple_first_item', 'tuple_second_item', 'tuple_third_item')
    my_class = MyClass('class string')
    comments = Comment.objects.all()
    return render(request, 'index.html', {
        'coms': comments,
        'my_str': my_str,
        'my_dict': my_dict,
        'my_list': my_list,
        'my_set': my_set,
        'my_tuple': my_tuple,
        'my_class': my_class,
        'display_num': True,
        'now': datetime.now()
    })


def test(request, bla):
    return render(request, 'test.html', {"text": bla})


def form_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # some actions
            return render(request, 'form_was_valid.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MyForm()

    return render(request, 'form.html', {'form': form})


def employee(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmployeeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # some actions
            return HttpResponseRedirect(reverse('congrats'))
        return HttpResponseRedirect(reverse('fail'))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeForm()

    return render(request, 'emloyee.html', {'form': form})


def fail(request):
    return render(request, 'fail.html')


def congrats(request):
    return render(request, 'congrats.html')


def my_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthenticationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # some actions
            login(request, form.user)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def my_register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # some actions
            user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                            password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def change_pass(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ChangePassForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # some actions
            user = request.user
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChangePassForm()
    return render(request, 'change-pass.html', {'form': form})


def comments_view(request):
    filter_text = request.GET.get('text', '')
    my = request.GET.get('my') == 'on'
    query = Q(text__icontains=filter_text)
    if my:
        query &= Q(user=request.user)
    comments = Comment.objects.filter(query)
    return render(request, 'comments.html', {"comments": comments, "form": CommentFilterForm()})


class MyView(View):
    pass