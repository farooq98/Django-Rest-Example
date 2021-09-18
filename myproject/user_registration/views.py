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
from django.conf import settings

root_path = os.getcwd()

workspace_login_link = ""

class CreateUser(APIView):

    authentication_classes = ()
    permission_classes = ()

    def validate_email(self, value):
        try:
            UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            return True
        else:
            return False

    def validate_password(self, value):
        passwd = len(value)
        if passwd and passwd < 8:
            return False
        return True
    
    def post(self, request):

        data = request.data
        email = data.get("email") if self.validate_email(data.get("email")) else False
        password = data.get("password") if self.validate_password(data.get("password")) else False

        if not email or not password:
            if not email:
                message = "Email is already taken"
            elif not password:
                message = "Password must be greater than 8 characters"

            return Response({
                "created": False,
                "message": message,
            }, status=status.HTTP_400_BAD_REQUEST)
        

        user = UserModel.objects.create_user(
            email=data.get("email"), 
            password=data.get("password")
        )    

        if user:
            user.designation = data.get("designation")
            user.name = data.get("name")
            user.save()
            return Response({
                "created": True,
                "message": "User Created",
                "verification_code": user.verification_code,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False,
                "message": "something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

class CreateWorkSpace(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        data = request.data

        if data.get('workspace_name'):
            image_name = root_path + "/workspace_images/" + data.get('workspace_name') + ".jpeg"
            with open(image_name, "wb") as fh:
                fh.write(decodebytes(data.get('workspace_image')))

        workspace_created = WorkSpaceModel.objects.create(
            workspace_name = data.get('workspace_name'),
            workspace_image = data.get('workspace_image'),
            user = request.user
        )

        if workspace_created:
            user_workspace_relation = UserWorkSpaceRelationTable.objects.create(
                user = request.user,
                workspace = workspace_created,
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
                login(request,user)
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

        if success and settings.DEBUG:
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

        try:
            user = UserModel.objects.get(email=eamil)
        except UserModel.DoesNotExist:
            return Response({
                "status": False,
                "isActive": False
            }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            auth_user = user.check_password(password)

            if auth_user:
                resp = {
                    "status": True,
                    "isActive": user.is_active
                }
                if user.is_active:
                    login(request, user)
                else:
                    user.send_email()
                    resp.update({"activation_code": user.code})

                try:
                    user_workspaces = UserWorkSpaceRelationTable.objects.filter(user=user)
                    user_workspaces = [{
                        "type_of_user": user_workspace.type_of_user,
                        "workspace_name": user_workspace.workspace.workspace_name,
                        "workspace_image": user_workspace.workspace.workspace_image,
                        "workspace_id": user_workspace.workspace.id,
                    } for user_workspace in user_workspaces]
                    resp.update({"user_workspaces":user_workspaces})
                except UserWorkSpaceRelationTable.DoesNotExist:
                    resp.update({"user_workspaces": []})
                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "isActive": user.is_active
                }, status=status.HTTP_400_BAD_REQUEST)
    
class ResendVerificationCode(APIView):

    def post(self, request):

        email = request.data.get('email')
        try:
            user = UserModel.objects.get(email=email)
            if not user.is_active:
                user.send_email()

                resp = {
                    'status': True,
                    'message': 'verification code sent'
                }
                if settings.DEBUG:
                    resp.update({'verfication_code': user.verification_code})

                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'message': 'user already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except UserModel.DoesNotExist:
            return Response({
                'status': False,
                'message': "so such user with email exists"
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

        data = []

        try:
            data = request.data
            members_email_list = data.get('emails')
            for email in members_email_list:
                try:
                    user = UserModel.objects.get(email=email)
                except UserModel.DoesNotExist:
                    password = generate_random_code(n_digits=8)
                    user = UserModel.objects.create_user(email=email, password=password)
                user.is_active = True
                user.save()

                if user:
                    user_workspace_relation = UserWorkSpaceRelationTable.objects.create(
                        user = user,
                        workspace = WorkSpaceModel.objects.get(int(data.get('workspace_id'))),
                        type_of_user='normal'
                    )
                    if user_workspace_relation:
                        if settings.DEBUG:
                            send_verification_email(email, password,'user invite', workspace_login_link)
                        else:
                            data.append({'email': email, 'password': password})

            resp = {
                "status": True,
                "message": "success"
            }

            if settings.DEBUG:
                resp.update({"data": data})
            
            return Response(resp, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status = status.HTTP_400_BAD_REQUEST)