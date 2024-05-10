from django.urls import path
from .views import NotificationCreateView, NotificationRetrieveView

urlpatterns = [
    path('create/', NotificationCreateView.as_view()),
    path('retrieve/<int:pk>/', NotificationRetrieveView.as_view()),
]
