from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from core.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import UserModel
from .serializers import UserSerializer

class CreateUser(APIView):
    
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({
                "status": True,
                "message": "An email with a verfication code has been sent to your email address"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False,
                "message": user.errors
            }, status=status.HTTP_400_BAD_REQUEST) 

class ActivateUser(APIView):
    
    def post(self, request):
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=request.data.get('email'))
            user.is_active = user.validate_timeout(str(request.data.get('verification_code')))
            
            if user.is_active:
                user.save()
                success, message, stat = True, "email has been verified", status.HTTP_200_OK
            else:
                success, message, stat = False, "verification code has expired", status.HTTP_400_BAD_REQUEST
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST

        return Response({
            "status": success,
            "message": message
        }, status=stat)

class ForgetPassword(APIView):
    
    def post(self, request):

        password = request.data.get('password')
        code = request.data.get('verification_code')
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=request.user.username)
            timeout_check = user.validate_timeout(code)
            
            if timeout_check:
                user.set_password(password)
                user.save()
                success, message, stat = True, "password has been changed", status.HTTP_200_OK
            else:
                success, message, stat = False, "verification code has expired", status.HTTP_400_BAD_REQUEST
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST

        return Response({
            "status": success,
            "message": message
        }, status=stat)

class LoginUser(APIView):
    
    def post(self, request):
        eamil = request.data.get('eamil')
        password = request.data.get('password')

        user = authenticate(username=eamil, password=password)

        if user:
            login(user)
            return Response({
                "status": True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False
            }, status=status.HTTP_400_BAD_REQUEST) 

class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response({'success':True, 'message': "Logout successfull."}, status=status.HTTP_200_OK)

class CheckAuth(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        return Response({'status': True, 'email': request.user.username}, status=status.HTTP_200_OK)
