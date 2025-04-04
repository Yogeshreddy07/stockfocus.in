from django.urls import path
from .views import learn_with_ai_view

urlpatterns = [
    path('', learn_with_ai_view, name='learn_with_ai'),
]