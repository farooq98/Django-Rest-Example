from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from core.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from base64 import decodebytes
from .models import UserModel
import os
from models.happyspace_models import WorkSpaceModel,UserWorkSpaceRelationTable
from .serializers import UserSerializer

root_path = os.getcwd()

class CreateUser(APIView):

<<<<<<< HEAD
    authentication_classes = ()
    permission_classes = ()
    
=======
>>>>>>> b318453c7c05f151797f096d4701beecdebd0e0b
    def post(self, request):

        data = request.data
        user = UserSerializer(data=request.data)
        image_name = root_path + "/workspace_images/" + data['workspace_name'] + ".jpeg"
        if user.is_valid():
            with open(image_name, "wb") as fh:
                fh.write(decodebytes(data['workspace_image']))
            workspace_created = WorkSpaceModel.objects.create(workspace_name=data['workspace_name'],
                                                              workspace_image=image_name,
                                                              user_id=user)

            if workspace_created:
                user_workspace_relation = UserWorkSpaceRelationTable.objects.create(user_id=user,
                                                                                    workspace_id=workspace_created,
                                                                                    type_of_user='admin')
                if user_workspace_relation:
                    user.save()

                    return Response({
                        "created": True,
                        "message": "Your " + data['workspace_name'] + " WorkSpace is Created."
                    }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False,
                "message": user.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ActivateUser(APIView):

    authentication_classes = ()
    permission_classes = ()
    
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

    authentication_classes = ()
    permission_classes = ()
    
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

    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):

        print(request.data)
        eamil = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=eamil, password=password)

        if user:
            login(request, user)
            return Response({
                "status": True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False
            }, status=status.HTTP_400_BAD_REQUEST) 

class LogoutView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        logout(request)
        return Response({'success':True, 'message': "Logout successfull."}, status=status.HTTP_200_OK)

class CheckAuth(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        return Response({'status': True, 'email': request.user.username}, status=status.HTTP_200_OK)
