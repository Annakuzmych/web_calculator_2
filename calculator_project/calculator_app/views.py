from .forms import ProUserForm,LoginForm,CalculatorForm,HistoryFilterForm,ProUser
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash,logout
from django.contrib.auth.models import Group
from .models import CalculationHistory, ConversionHistory
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Message
from asgiref.sync import async_to_sync


def home(request):
    return render(request, 'home.html')
def redoc(request):
    return render(request, 'redoc.html')
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = ProUserForm(data=request.POST)
        if form.is_valid():  
            user = form.save()
            login(request, user)
            return redirect('profile')
        else: print(form.errors)
    else:
        form = ProUserForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                print(1)
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

from django.shortcuts import render
import math
@csrf_exempt
def calculator(request):
    result = None
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            print(1)
            number1 = form.cleaned_data['number1']
            operator = form.cleaned_data['operator']
            number2 = form.cleaned_data.get('number2')
            if operator == 'sqrt':
                result = math.sqrt(number1)
            elif operator == 'sin':
                print(1)
                result = math.sin(math.radians(number1))
            elif operator == 'cos':
                result = math.cos(math.radians(number1))
            elif operator == 'tan':
                result = math.tan(math.radians(number1))
            elif operator == '%':
                result = number1 * (number2 / 100)
            elif operator in ['+', '-', '*', '/']:
                if number2 is None:
                    result = 'Error: Enter Number 2 for this operation'
                elif operator == '/' and number2 == 0:
                    result = 'Error: Division by zero'
                else:
                    result = eval(f'{number1} {operator} {number2}')
            print(1)
            user = request.user  # Отримання поточного користувача
            expression = f'{number1} {operator} {number2}' if number2 is not None else f'{operator} {number1}'
            # Створення екземпляру CalculationHistory та збереження його в базі даних
            print(1)
            calculation_history = CalculationHistory(user=user, expression=expression, result=result)
            calculation_history.save()
    else:
        form = CalculatorForm()
    return render(request, 'calculator.html', {'form': form, 'result': result})
def binary_to_decimal(binary_number):
    return int(binary_number, 2)

def binary_to_hex(binary_number):
    return hex(int(binary_number, 2))

def decimal_to_binary(decimal_number):
    return bin(decimal_number)

def decimal_to_hex(decimal_number):
    return hex(decimal_number)

def hex_to_binary(hex_number):
    return bin(int(hex_number, 16))

def hex_to_decimal(hex_number):
    return int(hex_number, 16)

def convert_number(number, from_base, to_base):
    if from_base == 2 and to_base == 10:
        return binary_to_decimal(number)
    elif from_base == 2 and to_base == 16:
        return binary_to_hex(number)
    elif from_base == 10 and to_base == 2:
        return decimal_to_binary(number)
    elif from_base == 10 and to_base == 16:
        number = int(number)
        return decimal_to_hex(number)
    elif from_base == 16 and to_base == 2:
        return hex_to_binary(number)
    elif from_base == 16 and to_base == 10:
        return hex_to_decimal(number)
    else:
        return "Conversion not supported"
@csrf_exempt
def number_converter(request):
    if request.method == 'POST':
        number = request.POST.get('number', '')
        from_base = int(request.POST.get('from_base', '10'))
        to_base = int(request.POST.get('to_base', '10'))
        user = request.user
        # Convert number from one base to another
        result=convert_number(number, from_base, to_base)
        conversion_history = ConversionHistory(user=user, number=number, from_base=from_base, to_base=to_base, result=result)
        conversion_history.save()
        return render(request, 'number_converter.html', {'converted_number': result})

    return render(request, 'number_converter.html', {})

@csrf_exempt   
@login_required
def history_view(request):
 # Отримати поточного користувача
    current_user = request.user

        # Отримати історію простих операцій для поточного користувача
    simple_operations = CalculationHistory.objects.filter(user=current_user)

        # Отримати історію переводу систем числення для поточного користувача
    number_conversions = ConversionHistory.objects.filter(user=current_user)

        # Передати дані в шаблон для відображення
    return render(request, 'history.html', {'simple_operations': simple_operations, 'number_conversions': number_conversions})

@csrf_exempt
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProUserForm(request.POST, instance=user)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            if new_username != user.username:
                form.add_error('username', 'You cannot change your username.')
                return render(request, 'edit_profile.html', {'form': form})
            else:
                # Збереження форми без збереження юзернейму
                form.save(commit=False)
                form.instance.username = user.username
                form.save()
                return redirect('profile')
        else: print(form.errors)
    else:
        form = ProUserForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)  # Викликайте функцію logout
    return redirect('register')

@login_required
def delete_profile(request):
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'Your account was deleted successfully!')
    return redirect('register')
@csrf_exempt
def clear_history(request):
    if request.method == 'POST':
        # Очищення історії
        CalculationHistory.objects.all().delete()
        ConversionHistory.objects.all().delete()
        # Перенаправлення користувача на сторінку, де можна переглянути оновлену історію
        return redirect('history_view')

    return render(request, 'clear_history.html')
@login_required
def chat(request):
    return render(request, 'chat.html', {'username': request.user.username})
def get_messages_for_room(request, room_name):
    messages = Message.objects.filter(room_name=room_name)
    data = [{'message': msg.message, 'username': msg.user.username} for msg in messages]
    return JsonResponse(data, safe=False)
from django.contrib.auth.decorators import user_passes_test
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)
@admin_required
def online_users_view(request):
    return render(request, 'online_users.html')

