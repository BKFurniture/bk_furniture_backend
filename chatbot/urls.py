from django.urls import path

from .views import ChatbotView

urlpatterns = [
    path('answer/', ChatbotView.as_view()),
]
