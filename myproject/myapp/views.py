from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from .send_email import email
from .serializers import TestSerializer
from .models import TestModel

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
            email(emails)
            return Response({
                "sent": True,
                "message": "success"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "sent": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    

