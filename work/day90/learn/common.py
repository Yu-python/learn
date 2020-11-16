from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.authentication import get_authorization_header, jwt_get_username_from_payload
from .models import User
import jwt


def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    print(exc, 11111)
    response = exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is None:
        response = Response(data={'code': 999, 'msg': '未知错误'})

    return response


# 认证类
class MyJSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # jwt_value = get_authorization_header(request) # 原生的
        jwt_value = request.data.get('token')
        print(jwt_value)

        # if not jwt_value:
        #     raise AuthenticationFailed('Token 字段是必须的')
        try:
            payload = jwt_decode_handler(jwt_value)
        except Exception:
            raise AuthenticationFailed('用户名或者密码错误')
        #     raise AuthenticationFailed('签名过期')
        # except jwt.InvalidTokenError:
        #     raise AuthenticationFailed('非法用户')
        username = jwt_get_username_from_payload(payload)
        # print(username)
        user = User.objects.filter(username=username).first()
        return user, jwt_value


class APIResponse(Response):

    def __init__(self, data=None,msg=None,status=None):
        dic1 = {'code': 100, 'data': data,'msg':msg}
        super(APIResponse, self).__init__( data=dic1,status=status, template_name=None, headers=None,
                                          exception=False, content_type=None)
