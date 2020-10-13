
from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, MeAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='user_registration'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('me/', MeAPIView.as_view(), name='user_me')
]
