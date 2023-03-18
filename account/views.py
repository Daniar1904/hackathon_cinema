from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from . import serializers
from .send_email import send_reset_email, send_confirmation_email
from Cinema.tasks import send_confirm_email_task

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=serializers.RegisterSerializer())
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                try:
                    # send_confirmation_email(user.email, user.activation_code)
                    send_confirm_email_task.delay(user.email, user.activation_code)
                except:
                    return Response({'msg': 'Register but trouble with mail!',
                                     'data': serializer.data}, status=201)
                return Response(serializer.data, status=201)
            return Response('Bad request!', status=400)


class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            return Response({'msg': 'Successfully activated!'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Link expired!'}, status=400)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class LogoutView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully logged out!', status=200)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=serializers.ForgotPasswordSerializer())
    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = serializer.data.get('email')
            user = User.objects.get(email=email)
            user.create_activation_code()
            user.save()
            send_reset_email(user)
            return Response('Check your email, we send a code', status=200)
        except User.DoesNotExist:
            return Response('User with this email does not exist', status=400)


class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=serializers.RestorePasswordSerializer())
    def post(self, request):
        serializer = serializers.RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password changed successfully!')


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


