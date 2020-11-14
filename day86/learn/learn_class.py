from rest_framework import authentication
from . import models
from rest_framework import exceptions


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token')
        if token:
            user = models.User.objects.filter(user_token=token).last()
            if user:
                return user,token
            else:
                raise exceptions.AuthenticationFailed('用户名或者密码错误')
        else:
            # 这个异常类继承了APIException这个类，所以在全局能捕获到
            raise exceptions.AuthenticationFailed('请你登录')