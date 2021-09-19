from .models import UserModel, WorkSpaceModel, UserWorkSpaceRelationTable
from core import generate_random_code,send_verification_email
from core.authentication import PublicAPI, PrivateAPI
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from base64 import decodebytes
import os

root_path = os.getcwd()

workspace_login_link = ""

class CreateUser(PublicAPI):

    @classmethod
    def validate_email(cls, value):
        try:
            UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            return True
        else:
            return False

    @classmethod
    def validate_password(cls, value):
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

            resp = {
                "created": True,
                "message": "User Created"
            }
            if settings.DEBUG:
                resp.update({"verification_code": user.verification_code})

            return Response(resp, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False,
                "message": "something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

class CreateWorkSpace(PrivateAPI):

    def post(self, request):

        data = request.data
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
                    "workspace_id": workspace_created.id,
                    "workspace_name": workspace_created.workspace_name,
                }, status = status.HTTP_201_CREATED)
        return Response({
            "status": False,
        }, status = status.HTTP_400_BAD_REQUEST)       

class ActivateUser(PublicAPI):

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

        resp = {
            "status": success,
            "message": message
        }

        if success:
            resp.update({"name": user.name, "designation": user.designation})

        return Response(resp, status=stat)

class RequestForgetPassword(PublicAPI):

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
            resp.update({"otp_code": user.verification_code, 'link': f"HappySpace://forgot/{email}/{user.verification_code}/"})

        return Response(resp, status=stat)


class ForgetPassword(PublicAPI):
    
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

class LoginUser(PublicAPI):

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
                    "isActive": user.is_active,
                    "name": user.name,
                    "designation": user.designation,
                    "image_url": user.image_url,
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
    
class ResendVerificationCode(PublicAPI):

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

class LogoutView(PublicAPI):

    def post(self, request):
        logout(request)
        return Response({'success':True, 'message': "Logout successfull."}, status=status.HTTP_200_OK)

class CheckAuth(PrivateAPI):

    def get(self, request):

        return Response({'status': True, 'email': request.user.username}, status=status.HTTP_200_OK)

class AddMembersWorkSpace(PrivateAPI):

    def post(self,request):

        invited_users = []

        try:
            data = request.data
            try:
                relation_obj = UserWorkSpaceRelationTable.objects.get(
                    workspace__id=int(data.get('workspace_id')),
                    user = request.user, 
                    type_of_user = 'admin'
                )
                wpmodel = relation_obj.workspace
            except WorkSpaceModel.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "workspace not found",
                }, status=status.HTTP_400_BAD_REQUEST)


            created_members = []
            
            members_email_list = data.get('emails')
            for email in members_email_list:
                try:
                    user = UserModel.objects.get(email=email)
                except UserModel.DoesNotExist:
                    password = generate_random_code(n_digits=8)
                    user = UserModel.objects.create_user(email=email, password=password)
                    created_members.append(user)
                user.is_active = True
                user.save()

                try:
                    UserWorkSpaceRelationTable.objects.get(user = user, workspace = wpmodel)
                except UserWorkSpaceRelationTable.DoesNotExist:
                    user_workspace_relation = UserWorkSpaceRelationTable.objects.create(
                        user = user,
                        workspace = wpmodel,
                        type_of_user = 'normal'
                    )
                    workspace_login_link = f"HappySpace://activate/{email}/{password}/" 
                    if user_workspace_relation and user_workspace_relation.user in created_members:
                        if not settings.DEBUG:
                            send_verification_email(email, password,'user invite', workspace_login_link)
                        else:
                            invited_users.append({'email': email, 'password': password, 'link': workspace_login_link})

            resp = {
                "status": True,
                "message": "success"
            }

            if settings.DEBUG:
                resp.update({"invited_users": invited_users})
            
            return Response(resp, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status = status.HTTP_400_BAD_REQUEST)

class UpdateUserDetails(PrivateAPI):

    def post(self, request):
        
        name = request.data.get('name')
        designation = request.data.get('designation')
        image_url = request.data.get('image_url')

        if name:
            request.user.name = name
        if designation:
            request.user.designation = designation
        if image_url:
            request.user.image_url = image_url


        request.user.save()

        return Response({
            "status": True,
            "message": "user info updated",
        }, status = status.HTTP_200_OK)

class ChangePassword(PrivateAPI):

    def post(self, request):

        password = request.data.get('password')

        if CreateUser.validate_password(password):

            request.user.set_password(str(password))
            request.user.save()

            return Response({
                'status': True,
                'message': 'success'
            }, status = status.HTTP_200_OK)
        
        else:
            return Response({
                'status': False,
                'message': 'password must be grater than 8 characters'
            }, status = status.HTTP_400_BAD_REQUEST)