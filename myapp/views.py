from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from core import test_email
from .serializers import TestSerializer
from .models import TestModel
from core.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .storage import decode_write_and_upload_image
class CustomPagination(PageNumberPagination):
    pagination_class = PageNumberPagination
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10 

class Test(ListAPIView):

    serializer_class = TestSerializer
    queryset = TestModel.objects.all()
    pagination_class = CustomPagination

class TestCreate(ListCreateAPIView):
    
    serializer_class = TestSerializer
    queryset = TestModel.objects.all()

class SendMessagesOnEmail(APIView):

    def post(self, request):
        emails = request.data.get("email")
        try:
            test_email(emails)
            return Response({
                "sent": True,
                "message": "success"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "sent": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UploadImageAndGetUrl(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        data = request.data
        if data.get("image_name"):
            image_url = decode_write_and_upload_image(data.get('image_name'))
            if image_url:
                resp = {"image_url":image_url}
                return Response({
                    "status": True,
                    "message":resp
                }, status = status.HTTP_200_OK
                )
            return Response({
                "status": False,
            }, status=status.HTTP_400_BAD_REQUEST)