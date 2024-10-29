from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from registration.models import CustomUser, Interest
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


@login_required
def cabinet(request):
    user = CustomUser.objects.get(id=request.session.get('user_id'))
    context = {
        'user': user,
    }

    return render(request, 'cabinet/cabinet.html', context)


def update_data(custom_user_model, interest_model, user_id):
    user = custom_user_model.objects.get(id=user_id)
    interest_list = interest_model.objects.all()

    context = {
        'user': user,
        'interest_list': interest_list,
    }
    return context


def update_password(old_password, new_password, user_id):
    user = CustomUser.objects.get(id=user_id)
    if check_password(old_password, user.password):
        user.set_password(new_password)
        user.save()
        return True
    else:
        return False


def change_data(request):

    user = CustomUser.objects.get(id=request.session.get('user_id'))
    context = update_data(CustomUser, Interest, user.id)

    if request.method == 'GET':
        for key in list(request.session.keys()):
            if 'errors_password' in key:
                context['errors_password'] = request.session.pop(key, None)
                break
            elif 'change_success' in key:
                context['change_success'] = request.session.pop(key, None)
                break

        return render(request, 'cabinet/change_data.html',
                      context)

    elif request.method == 'POST':
        first_name = request.POST.get('name')
        if first_name:
            CustomUser.objects.filter(id=user.id).update(first_name=first_name)

        last_name = request.POST.get('surname')
        if last_name:
            CustomUser.objects.filter(id=user.id).update(last_name=last_name)

        phone = request.POST.get('phone')
        if phone:
            CustomUser.objects.filter(id=user.id).update(phone=phone)

        email = request.POST.get('email')
        if email:
            CustomUser.objects.filter(id=user.id).update(email=email)
            CustomUser.objects.filter(id=user.id).update(username=email)

        interests = request.POST.getlist('tags[]')
        if interests:
            CustomUser.objects.filter(id=user.id).update(interests=interests)

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if old_password and new_password:
            if update_password(old_password, new_password, user.id):
                pass
            else:
                request.session['errors_password'] = 'Введите правильный пароль'
        elif old_password and new_password == '':
            request.session['errors_password'] = 'Введите новый пароль'
            return redirect('change_data')
        elif old_password == '' and new_password:
            request.session['errors_password'] = 'Введите старый пароль'
            return redirect('change_data')

        request.session['change_success'] = 'Изменения сохранены'
        return redirect('change_data')

    else:
        return JsonResponse({'success': False, 'error': 'Invalid change data'})


def logout_view(request):
    logout(request)
    return redirect('home')
