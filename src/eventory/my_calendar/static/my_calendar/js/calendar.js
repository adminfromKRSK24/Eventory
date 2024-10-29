const subscribeText = "Подписатьcя";
const unsubscribeText = "Отписатьcя";

if (window.innerWidth <= 400) {
    location.href = "#mainTable";
}

// Функция для обновления текста и классов кнопки
function updateButtonAppearance(button, isSubscribed) {
    // Обновляем текст кнопки в зависимости от состояния подписки
    button.innerHTML = isSubscribed ? unsubscribeText : subscribeText;

    // Обновляем классы для стилизации кнопки
    if (isSubscribed) {
        button.classList.remove('subscribed');
        button.classList.add('unsubscribed');
    } else {
        button.classList.remove('unsubscribed');
        button.classList.add('subscribed');
    }
}

document.addEventListener("DOMContentLoaded", function() {
        // Выбираем все кнопки с классом 'event-subscribe'
        const buttons = document.querySelectorAll('.event-subscribe');

        // Проходим по каждой кнопке, чтобы обновить ее состояние
        buttons.forEach(button => {
            updateButtonState(button);
        });
    });

function updateButtonState(button) {

    console.log("type sub:", button.getAttribute('data-subscribed'))
    let isSubscribed = button.getAttribute('data-subscribed') === 'True';

    updateButtonAppearance(button, isSubscribed)
}

function toggleSubscription(button) {
    const eventId = button.getAttribute('data-event-id');
    let subscribed = button.getAttribute('data-subscribed') === 'True';
    console.log("event:", eventId)
    console.log("subscribed:", subscribed)

    const data = {
        event_id: eventId,
        subscribe: !subscribed  // Инвертируем значение
    };

    console.log("data:", data)

    fetch('/calendar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Django CSRF token
        },
        body: JSON.stringify(data)
    })

    .then(response => response.json())

    .then(result => {
        console.log("result:", result.success)
        console.log("mes:", result.error)

        if (result.success) {
            // Обновить состояние кнопки
            const newSubscribedState = !subscribed;

            console.log("new:", newSubscribedState)

            button.setAttribute('data-subscribed', newSubscribedState ? 'True' : 'False');

            console.log("data-subscribed:", newSubscribedState.toString())

            let isSubscribed = button.getAttribute('data-subscribed') === 'True';
            updateButtonAppearance(button, isSubscribed)

        } else {
            console.error('Не удалось обновить подписку');
        }
    })
    .catch(error => console.error('Ошибка:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//html {
//    scroll-behavior: smooth; /* Плавная прокрутка при переходе по якорям */
//}
window.onload = function() {
    window.scrollTo(0, 0); // Прокрутка в начало страницы
};
window.onresize = function() {
    window.scrollTo(0, 0); // Прокрутка в начало страницы при изменении размера
};