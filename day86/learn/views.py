from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from . import learn_serializers
from rest_framework import mixins
from rest_framework.response import Response
from . import models
import uuid
from . import learn_class

class Login(APIView):
    msg = {
        'code': 200,
        'msg': None, }

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = models.User.objects.filter(username=username, password=password)
        if user_obj:
            # 使用uuid生成唯一token
            token = uuid.uuid4()
            user = user_obj.last()
            # 更新数据库中的token
            user.user_token=token
            user.save()
            print(user.user_token)
            self.msg['msg'] = '登录成功'
            self.msg['token'] = token
        else:
            self.msg['code']=100
            self.msg['msg']= '登录失败'

        return Response(self.msg)


class Book(GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    serializer_class = learn_serializers.BooksModelSerializer
    queryset = models.Book.objects.all()
    authentication_classes = [learn_class.TokenAuthentication]
