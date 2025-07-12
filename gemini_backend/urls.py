"""
URL configuration for gemini_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Gemini Backend Clone is running!',
        'version': '1.0.0'
    })

def db_check(request):
    """Database check endpoint"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
        
        return JsonResponse({
            'status': 'database_ok',
            'tables': tables,
            'message': f'Database has {len(tables)} tables'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'database_error',
            'error': str(e)
        }, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('chatroom/', include('chatrooms.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('health/', health_check, name='health_check'),
    path('db-check/', db_check, name='db_check'),
]
