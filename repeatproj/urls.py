
from django.contrib import admin
from django.urls import path
from repeatapp.views import RegisterView,LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/',RegisterView.as_view()),
    path('api/login/',LoginView.as_view())
]
