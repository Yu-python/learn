from django.shortcuts import render

# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from .serliazer import BookSerializer

class Book(APIView):
    def get(self,request,*args,**kwargs):
        query_set = models.Book.objects.all()
        serializer = BookSerializer(instance=query_set,many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookDetail(APIView):
    def get(self, request,pk, *args, **kwargs):
        query_set = models.Book.objects.get(pk=pk)
        serializer = BookSerializer(instance=query_set,)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        book_obj = models.Book.objects.get(pk=pk)
        serializer = BookSerializer(instance=book_obj,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pk,*args,**kwargs):
        models.Book.objects.filter(pk=pk).delete()
        return Response()