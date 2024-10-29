from django.shortcuts import render, HttpResponse, redirect
from .models import CustomUser, Interest, Event


def user_registration(request):

    if request.method == 'POST':
        t_password = request.POST.get('password')
        t_password_repeat = request.POST.get('password_repeat')
        if t_password_repeat != t_password:
            request.session['error_passw_repeat'] = 'Пароли не совпадают'
            return redirect('user_registration')
        try:
            user = CustomUser.objects.create_user(
                username=request.POST.get('email'),
                email=request.POST.get('email'),
                password=t_password,
                first_name=request.POST.get('name'),
                last_name=request.POST.get('surname'),
                phone=request.POST.get('phone'),
                interests=request.POST.getlist('tags[]')
            )
            return redirect('succ_reg')
        except Exception as e:
            return HttpResponse(f'Ошибка при создании пользователя: {str(e)}')

    interest_list = Interest.objects.all()
    error_passw_repeat = request.session.pop('error_passw_repeat', None)
    return render(request, 'registration/user_regs.html',
                  {'interest_list': interest_list, 'error_passw_repeat': error_passw_repeat})


def succ_reg(request):
    return render(request, 'registration/succ_reg.html')


def event_registration(request):
    interest_list = Interest.objects.all()
    error_interest = None
    try:
        if request.method == 'POST':
            interest_id = request.POST.get('tag')
            print(f"Interest ID: {interest_id}")
            if not interest_id:
                error_interest = 'Необходимо выбрать тематику мероприятия.'
                return render(request, 'registration/event_regs.html',
                              {'interest_list': interest_list, 'error_interest': error_interest})
            event = Event(
                title=request.POST.get('title'),
                date=request.POST.get('date'),
                time=request.POST.get('time'),
                organizer=request.POST.get('organizer'),
                interest_id=interest_id
            )
            event.save()
            return redirect('succ_event_reg')
    except Exception as e:
        return HttpResponse(f'Ошибка при создании мероприятия: {str(e)}')

    return render(request, 'registration/event_regs.html', {'interest_list': interest_list})


def succ_event_reg(request):
    return render(request, 'registration/succ_event_reg.html')
