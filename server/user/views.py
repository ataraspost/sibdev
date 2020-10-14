
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site

from .serializers import LoginSerializer
from .serializers import RegistrationSerializer
from.tasks import task_send_email
from user.models import EmailConfirmationToken

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

class ActivateEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            token = EmailConfirmationToken.objects.select_related('user').get(token=token)
        except EmailConfirmationToken.DoesNotExist:
            return Response({
            'message': 'error email activate'
        }, status=status.HTTP_400_BAD_REQUEST)
        user = token.user
        user.email_is_activate = True
        user.save()
        token.delete()
        return Response({
            'message': 'email activate'
        }, status=status.HTTP_200_OK)
