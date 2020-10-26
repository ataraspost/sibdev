
from django.urls import path

from .views import (RegistrationAPIView, LoginAPIView, MeAPIView, ActivateEmailAPIView,
                    UserSimilarityAPIView, PrecedentAPIView,)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='user_registration'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('me/', MeAPIView.as_view(), name='user_me'),
    path('activate-email/<slug:token>', ActivateEmailAPIView.as_view(), name='user_activate_email'),
    path('user/<int:pk>/similirity/', UserSimilarityAPIView.as_view(), name='user_similarity'),
    path('precedent/', PrecedentAPIView.as_view(), name='user-precedent'),
    path('precedent/<int:pk>/', PrecedentAPIView.as_view(), name='user-precedent'),
]

