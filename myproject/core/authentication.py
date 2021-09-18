from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


class CsrfExemptSessionAuthentication(SessionAuthentication):
    
    def enforce_csrf(self, request):
        return

class NoAuth:
    
    authentication_classes = ()
    permission_classes = ()

class Auth:
    
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

class PublicAPI(APIView, NoAuth):
    
    authentication_classes = ()
    permission_classes = ()

class PrivateAPI(APIView, Auth):
    
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

class PrivateListAPI(ListAPIView, Auth):
    
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

class ListPublicAPI(ListAPIView, NoAuth):
    
    authentication_classes = ()
    permission_classes = ()