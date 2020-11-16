from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from . import learn_class
from rest_framework.views import APIView
from .common import MyJSONWebTokenAuthentication
from . import models
from .common import APIResponse


class Login(ViewSet):

    def create(self, request, *args, **kwargs):
        login_serializer = learn_class.LoginModelSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        # login_serializer.save() # 这是一个坑呀，不能保存
        context = login_serializer.context
        return Response(context)


class Test(APIView):
    authentication_classes = [MyJSONWebTokenAuthentication, ]

    def get(self, request, *args, **kwargs):
        return APIResponse(data='这个一个测试语句')


class Book(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Book.objects.get(pk=pk)
            ser = learn_class.BookSerializer(instance=book_obj)
        else:
            book_obj = models.Book.objects.all()
            ser = learn_class.BookSerializer(instance=book_obj, many=True)

        return APIResponse(ser.data)

    def post(self,request, *args, **kwargs):
        print(len(request.data))
        if isinstance(request.data,list):
            ser = learn_class.BookSerializer(data=request.data, many=True)
        else:
            ser = learn_class.BookSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return APIResponse(ser.data)

    def delete(self, request, *args, **kwargs):
        pk = request.data.get('pk')


        if isinstance(pk,list): # {"pk":[20,21,18]}
            models.Book.objects.filter(pk__in=pk).update(is_delete=True)
            length = len(pk)
        else:
            length = 1
            models.Book.objects.filter(pk=pk).update(is_delete=True)

        data = '%s条数据该变了' % length
        return APIResponse(data=data)

    '''
    {
        "title": "linux",
        "price": "88.00",
        "publishes": 2,
        "author": 
            [1,3] 
    }
    '''


    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Book.objects.get(pk=pk)
            ser = learn_class.BookSerializer(instance=book_obj,data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return APIResponse(ser.data)

        else:
            pks = []
            for item in request.data:
                pks.append(item['id'])
                item.pop('id')
            book_list = models.Book.objects.filter(id__in=pks, is_delete=False)

            for i,book in enumerate(book_list):
                ser = learn_class.BookSerializer(instance=book, data=request.data[i])
                ser.is_valid(raise_exception=True)
                ser.save()

            return Response(data='影响的行数%s' % len(pks))



class Publish(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Publish.objects.get(pk=pk)
            ser = learn_class.PublishSerializer(instance=book_obj)
        else:
            book_obj = models.Publish.objects.all()
            ser = learn_class.PublishSerializer(instance=book_obj, many=True)

        return APIResponse(ser.data,msg='ok')

    def post(self,request, *args, **kwargs):
        print(len(request.data))
        if isinstance(request.data,list):
            ser = learn_class.PublishSerializer(data=request.data, many=True)
        else:
            ser = learn_class.PublishSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return APIResponse(ser.data)
    #
    def delete(self, request, *args, **kwargs):
        pk = request.data.get('pk')

        if isinstance(pk,list): # {"pk":[20,21,18]}
            models.Publish.objects.filter(pk__in=pk).update(is_delete=True)
            length = len(pk)
        else:
            length = 1
            models.Publish.objects.filter(pk=pk).update(is_delete=True)

        data = '%s条数据该变了' % length
        return APIResponse(data=data)

    # '''
    # {
    #     "title": "linux",
    #     "price": "88.00",
    #     "publishes": 2,
    #     "author":
    #         [1,3]
    # }
    # '''


    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Publish.objects.get(pk=pk)
            ser = learn_class.PublishSerializer(instance=book_obj,data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return APIResponse(ser.data)

        else:
            print(request.data)
            pks = []
            for item in request.data:
                pks.append(item['id'])
                item.pop('id')
            book_list = models.Publish.objects.filter(id__in=pks, is_delete=False)

            for i,publish in enumerate(book_list):
                ser = learn_class.PublishSerializer(instance=publish, data=request.data[i])
                ser.is_valid(raise_exception=True)
                ser.save()

            return Response(data='影响的行数%s' % len(pks))


class Author(APIView):


    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Author.objects.get(pk=pk)
            ser = learn_class.AuthorSerializer(instance=book_obj)
        else:
            book_obj = models.Author.objects.all()
            ser = learn_class.AuthorSerializer(instance=book_obj, many=True)

        return APIResponse(ser.data,msg='ok')


    def post(self,request, *args, **kwargs):
        print(len(request.data))
        if isinstance(request.data,list):
            ser = learn_class.AuthorSerializer(data=request.data, many=True)
        else:
            ser = learn_class.AuthorSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return APIResponse(ser.data)
    #
    def delete(self, request, *args, **kwargs):
        pk = request.data.get('pk')

        if isinstance(pk,list): # {"pk":[20,21,18]}
            models.Author.objects.filter(pk__in=pk).update(is_delete=True)
            length = len(pk)
        else:
            length = 1
            models.Author.objects.filter(pk=pk).update(is_delete=True)

        data = '%s条数据该变了' % length
        return APIResponse(data=data)

    # '''
    # {
    #     "title": "linux",
    #     "price": "88.00",
    #     "publishes": 2,
    #     "author":
    #         [1,3]
    # }
    # '''


    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Author.objects.get(pk=pk)
            ser = learn_class.AuthorSerializer(instance=book_obj,data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return APIResponse(ser.data)

        else:
            print(request.data)
            pks = []
            for item in request.data:
                pks.append(item['id'])
                item.pop('id')
            author_list = models.Author.objects.filter(id__in=pks, is_delete=False)

            for i,publish in enumerate(author_list):
                ser = learn_class.AuthorSerializer(instance=publish, data=request.data[i])
                ser.is_valid(raise_exception=True)
                ser.save()

            return Response(data='影响的行数%s' % len(pks))
