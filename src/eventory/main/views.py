import logging
from distutils.command.check import check
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from registration.models import CustomUser
from django.contrib.auth.hashers import check_password


# Настройка логирования
logger = logging.getLogger(__name__)

def index(request):

    if request.method == 'POST':
        # Обработка POST-запроса
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Аутентификация пользователя
            user = authenticate(request, username=username, password=password)

            # Проверка, что пользователь найден
            if user is not None:
                login(request, user)  # Авторизация пользователя

                # Дополнительно можно сохранять информацию в сессии
                request.session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
                request.session['username'] = user.username  # Сохраняем имя пользователя в сессии

                return redirect('cabinet')
            else:
                request.session['errors_incorrect'] = 'Почта или пароль не верны'
                return redirect('home')
        except CustomUser.DoesNotExist:
            request.session['errors_incorrect'] = 'Почта или пароль не верны'
            return redirect('home')

    errors_incorrect = request.session.pop('errors_incorrect', None)
    return render(request, 'main/index.html', {'errors_incorrect': errors_incorrect})


def about(request):
    return render(request, 'main/about.html')
