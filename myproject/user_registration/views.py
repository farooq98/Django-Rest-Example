from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserModel
from .serializers import UserSerializer

class CreateUser(APIView):
    
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({
                "created": True,
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
            user.is_active = user.verify_email_code(str(request.data.get('verification_code')))
            
            if user.is_active:
                user.save()
                success, message, stat = True, "email has been verified", status.HTTP_200_OK
            else:
                success, message, stat = False, "verification code has expired", status.HTTP_400_BAD_REQUEST
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST

        return Response({
            "success": success,
            "message": message
        }, status=stat)