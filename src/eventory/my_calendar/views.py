import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registration.models import CustomUser
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Event, EventUser, get_all_events_by_month

@login_required
def my_calendar(request):
    user_in_ses = CustomUser.objects.get(id=request.session.get('user_id'))  # добавил
    data = {}
    if request.method == 'POST':
        # Обработка POST-запроса для обновления подписки
        try:
            data = json.loads(request.body)

            if not request.body:
                return JsonResponse({'success': False, 'error': 'Empty request body'})


            # if not request.user.is_authenticated:
            #     return JsonResponse({"success": False "error": "User is not authenticated"})


            user_id = user_in_ses.id  # было: request.user.id
            # user_id = request.POST.get('user_id')

            event_id = data.get('event_id')
            subscribe = data.get('subscribe')

            # Проверка на наличие event_id и subscribe
            if event_id is None or subscribe is None:
                return JsonResponse({'success': False, 'error': 'Missing required data'})

            # Получаем объект пользователя
            user = get_object_or_404(CustomUser, id=user_id)

            # Получаем объект события
            event = get_object_or_404(Event, id=event_id)

            # Получаем или создаем объект EventUser
            event_user, created = EventUser.objects.get_or_create(event_id=event, user_id=user)

            # Обновляем поле подписки
            event_user.subscribe = subscribe
            event_user.save()

            # # Возврат JSON-ответа о успешном обновлении
            return JsonResponse({'success': True, "response": "успешно"})

        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'})
        except json.JSONDecodeError:
            if not request.body:
                return JsonResponse({'success': False, 'error': 'Empty request body'})

            # Проверка на наличие event_id и subscribe
            if data.get('event_id') is None or data.get('subscribe') is None:
                return JsonResponse({'success': False, 'error': 'Missing required data'})

            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})


    if request.method == 'GET':
        # Обработка GET-запроса
        # events = get_all_events_grouped_by_month()
        try:
            events = get_all_events_by_month(user_in_ses)
            return render(request, 'my_calendar/my_calendar.html', {'events': events})
        except CustomUser.DoesNotExist:
            messages.error(request, "Пользователь не найден.")
            return render(request, 'user_not_found.html', status=404)
    else:
        return JsonResponse({'success': True})





