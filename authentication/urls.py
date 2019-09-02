from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import signup, activate, activation_email_sent


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='cauth2/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path(r'activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('activation_email_sent/', activation_email_sent, name='activation_email_sent')
]
