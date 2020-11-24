from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import settings, notifications_settings, sign_in, sign_up, profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('notifications_settings', notifications_settings,
         name='notifications_settings'),
    path('profile', profile, name='profile'),
    path('settings', settings, name='settings'),
    path('sign_in', sign_in, name='sign_in'),
    path('sign_up', sign_up, name='sign_up'),
    path('MainApp/', include('MainApp.urls')),
]
