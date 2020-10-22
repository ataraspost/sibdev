
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site

from .serializers import LoginSerializer, RegistrationSerializer, PrecedentSerializer, UserSerializer
from.tasks import task_send_email
from user.models import EmailConfirmationToken, Precedent

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


class PrecedentAPIView(APIView):
    def get_object(self, pk):
        try:
            return Precedent.objects.get(pk=pk)
        except Precedent.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk is not None:
            precedent = self.get_object(pk)
            assert request.user == precedent.user
            serializer = PrecedentSerializer(precedent)
            return Response(serializer.data)
        precedent = Precedent.objects.all().filter(user=request.user)
        serializer = PrecedentSerializer(precedent, many=True)
        return Response(serializer.data)

    def post(self, request):

        data = {
            'name': request.data['name'],
            'positive': request.data['positive'],
            'importance': request.data['importance'],
            'user': request.user.id,
        }
        serializer = PrecedentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        precedent = self.get_object(pk)
        assert request.user == precedent.user
        data = {
            'name': request.data.get('name', precedent.name),
            'positive': request.data.get('positive', precedent.positive),
            'importance': request.data.get('importance', precedent.importance),
            'user': request.user.id,
        }
        serializer = PrecedentSerializer(data=data)
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        precedent = self.get_object(pk)
        assert request.user == precedent.user
        precedent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSimilarityAPIView(APIView):

    def get(self, request):
        return Response({'user': self.request.user.email, 'token': self.request.user.token}, status=status.HTTP_200_OK)

class UserSimilarityWithRedisAPIView(APIView):

    def get(self, request):
        return Response({'user': self.request.user.email, 'token': self.request.user.token}, status=status.HTTP_200_OK)
