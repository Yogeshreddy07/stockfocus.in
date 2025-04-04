"""geeksforgeeks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ollama_chat
from stockfocusin.views import learn_with_ai

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line
    path('LearnWithAI/', learn_with_ai, name='learn_with_ai'),  # Updated to match the browser request
    path('api/ollama/', ollama_chat, name='ollama_chat'),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

