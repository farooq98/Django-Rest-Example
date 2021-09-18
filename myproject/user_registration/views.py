from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from core.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from base64 import decodebytes
from .models import UserModel, WorkSpaceModel, UserWorkSpaceRelationTable
import os
from core import generate_random_code,send_verification_email
from .serializers import UserSerializer

root_path = os.getcwd()

workspace_login_link = ""

class CreateUser(APIView):

    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):

        data = request.data
        user = UserSerializer(data = request.data)
        if user.is_valid():
            return Response({
                "created": True,
                "message": "User Created"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False,
                "message": user.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class CreateWorkSpace(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        data = request.data
        
        image_name = root_path + "/workspace_images/" + data.get('workspace_name') + ".jpeg"

        with open(image_name, "wb") as fh:
            fh.write(decodebytes(data.get('workspace_image')))
        workspace_created = WorkSpaceModel.objects.create(
            workspace_name = data.get('workspace_name'),
            workspace_image = image_name,
            user_id = request.user
        )

        if workspace_created:
            user_workspace_relation = UserWorkSpaceRelationTable.objects.create(
                user_id = request.user,
                workspace_id = workspace_created,
                type_of_user = 'admin'
            )
            if user_workspace_relation:
                request.user.is_workspace_admin = True
                request.user.save()

                return Response({
                    "status": True,
                }, status = status.HTTP_201_CREATED)
        return Response({
            "status": False,
        }, status = status.HTTP_400_BAD_REQUEST)

            

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

class RequestForgetPassword(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        email = request.data.get('email')
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=email)
            user.change_password()

            success, message, stat = True, "an email with otp code is sent", status.HTTP_200_OK
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST
        
        resp = {
            "status": success,
            "message": message,
        }

        if success:
            resp.update({"otp_code": user.verification_code})

        return Response(resp, status=stat)


class ForgetPassword(APIView):

    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('verification_code')
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=email)
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
                "status": False,
                "isActive": user.is_active
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

class AddMembersWorkSpace(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self,request):

        data = request.data
        members_email_list = data['emails']
        for email in members_email_list:
            password = generate_random_code(n_digits=8)
            user = UserModel.objects.get_or_create(email,password)

            if user:
                user_workspace_relation = UserWorkSpaceRelationTable.objects.create(
                    user_id= user,
                    workspace_id=data.get('workspace_id'),
                    type_of_user='normal'
                )
                if user_workspace_relation:
                    send_verification_email(email,password,'user invite',workspace_login_link)

        return Response({"status": True
                            }, status=status.HTTP_201_CREATED)