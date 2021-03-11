from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class MyForm(forms.Form):
    nickname = forms.CharField(label='My nickname', max_length=100)
    age = forms.IntegerField(label='My age')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age % 2:
            raise ValidationError('Age should be odd')
        return age

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        nickname = cleaned_data.get('nickname')
        if str(age) in nickname:
            self.add_error('age', 'Age cannot be in nickname')
        self.add_error(None, 'This form always incorrect')


class EmployeeForm(forms.Form):
    SEX = ((1, 'Man'),
           (2, 'Woman'))
    ENGLISH = (
        (1, 'A1'),
        (2, 'A2'),
        (3, 'B1'),
        (4, 'B2'),
        (5, 'C1'),
        (6, 'C2'),
    )

    name = forms.CharField(max_length=50)
    age = forms.IntegerField(min_value=18, max_value=99)
    sex = forms.ChoiceField(choices=SEX)
    english = forms.ChoiceField(choices=ENGLISH)

    def clean(self):
        cd = super().clean()
        if not (cd.get('sex') == '1' and cd.get('age') >= 20 and int(cd.get('english')) >= 4) and not (
                cd.get('sex') == '2' and cd.get('age') >= 22 and int(cd.get('english')) >= 3):
            raise ValidationError('Not our candidate')


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise forms.ValidationError('Login/Password is incorrect')


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('Passwords not equal')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            raise ValidationError('User with this username already exist')


class ChangePassForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('Passwords not equal')


class CommentFilterForm(forms.Form):
    text = forms.CharField(label='Filter text')
    my = forms.BooleanField(required=False)
