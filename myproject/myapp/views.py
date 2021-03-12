from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import TestSerializer
from .models import TestModel

class Test(ListAPIView):

    serializer_class = TestSerializer
    queryset = TestModel.objects.all()


