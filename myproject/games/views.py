from core.authentication import PrivateAPI
from rest_framework.response import Response
from rest_framework import status
from user_registration.models import UserWorkSpaceRelationTable
from .models import UserQuestions

# Create your views here.

class GetAllUsersWithQuiz(PrivateAPI):
    
    def get(self, request):

        try:
            UserWorkSpaceRelationTable.objects.get(
                workspace__id = request.GET.get('workspace_id'), 
                user = request.user
            )
        except UserWorkSpaceRelationTable.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid workspace"
            }, status=status.HTTP_400_BAD_REQUEST)

        workspace_users = [obj.user for obj in UserWorkSpaceRelationTable.objects.filter(
            workspace__id = request.GET.get('workspace_id')
        )]

        return Response([{
            'user_id': usr.id,
            'email': usr.email
        } for usr in UserQuestions.objects.filter(user__in=workspace_users)], status=status.HTTP_200_OK)

