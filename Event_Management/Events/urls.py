from django.urls import path
from .views import event_list,event_detail,event_register,unregister_from_event,user_dashboard

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('<int:pk>/register/', event_register, name='event_register'),
    path('<int:pk>/unregister/', unregister_from_event, name='unregister_from_event'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
]