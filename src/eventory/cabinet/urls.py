from django.urls import path
from . import views
from registration.views import event_registration

urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('changedata/', views.change_data, name='change_data'),
    path('event_registration/', event_registration, name='event_registration'),
    path('logout/', views.logout_view, name='logout'),
]
