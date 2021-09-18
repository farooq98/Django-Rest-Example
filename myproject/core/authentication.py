from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class CsrfExemptSessionAuthentication(SessionAuthentication):
    
    def enforce_csrf(self, request):
        return

class PublicAPI(APIView):

    authentication_classes = ()
    permission_classes = ()

class PrivateAPI(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )