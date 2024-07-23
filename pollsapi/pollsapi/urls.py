"""
URL configuration for pollsapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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


# re-path: 정규식을 사용하여 URL 패턴 정의
# path: 단순 경로 문자열 사용, 빈 문자열은 루트 URL을 정의함
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
]
