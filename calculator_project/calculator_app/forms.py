from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import ProUser,Message

class ProUserForm(UserCreationForm):
    class Meta:
        model = ProUser
        fields = ('username', 'gender', 'date_of_birth','email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(ProUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)


OPERATORS = [
    ('+', '+'),
    ('-', '-'),
    ('*', '*'),
    ('/', '/'),
    ('sqrt', 'sqrt'),
    ('sin', 'sin'),
    ('cos', 'cos'),
    ('tan', 'tan'),
    ('%', '%'),
]

class CalculatorForm(forms.Form):
    number1 = forms.FloatField(label='Number 1')
    operator = forms.ChoiceField(choices=OPERATORS)
    number2 = forms.FloatField(label='Number 2', required=False)


class NumberConversionForm(forms.Form):
    number = forms.CharField(label='Number', max_length=100)
    from_base = forms.ChoiceField(choices=[(2, 'Binary'), (8, 'Octal'), (10, 'Decimal'), (16, 'Hexadecimal')], label='From Base')
    to_base = forms.ChoiceField(choices=[(2, 'Binary'), (8, 'Octal'), (10, 'Decimal'), (16, 'Hexadecimal')], label='To Base')

class HistoryFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False)
    end_date = forms.DateField(label='End Date', required=False)
    calculation_type = forms.ChoiceField(choices=[('', 'All'), ('calculation', 'Calculation'), ('conversion', 'Conversion')], required=False)
