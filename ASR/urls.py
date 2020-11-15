from django.contrib import admin
from django.urls import path, include
# from . import settings, notifications_settings, sign_in, sign_up
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('notifications_settings', notifications_settings,
    #      name='notifications_settings'),
    # path('profile', profile, name='profile'),
    # path('settings', settings, name='settings'),
    # path('sign_in', sign_in, name='sign_in'),
    # path('sign_up', sign_up, name='sign_up'),
    path('MainApp/', include('MainApp.urls')),
]
