
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site

from .serializers import LoginSerializer
from .serializers import RegistrationSerializer
from.tasks import task_send_email

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        domain = get_current_site(request).domain
        task_send_email.delay(user.id, domain)
        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MeAPIView(APIView):

    def get(self, request):
        return Response({'user': self.request.user.email, 'token': self.request.user.token}, status=status.HTTP_200_OK)

class ActivateEmail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        return Response({
            'user': user.email
        })
