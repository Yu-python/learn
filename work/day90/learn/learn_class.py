from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


#
# class LoginModelSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     # password = serializers.CharField()
#
#     class Meta:
#
#         model = models.User
#         fields = ['username', 'password']
#         # extra_kwargs = {
#         #                  'username':{'write_only':True},
#         #                  'password':{'write_only':True}
#         #                },
#
#     def validate(self, attrs):
#
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         if username.isdigit():
#             user_obj = models.User.objects.get(mobile=username)
#         elif '@' in username:
#             user_obj = models.User.objects.get(email=username)
#         else:
#             user_obj = models.User.objects.get(username=username)
#
#         if not user_obj and user_obj.check_password(password):
#             raise ValidationError('用户名或者密码错误')
#         user = user_obj
#
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         self.context.update({'token':token,'username':user.username})
#
#         return attrs


class LoginModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    # password = serializers.CharField()

    class Meta:

        model = models.Userinfo
        fields = ['username', 'password']
        # extra_kwargs = {
        #                  # 'username':{'write_only':True},
        #                  'password':{'write_only':True}
        #                },

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        if username.isdigit():
            user_obj = models.Userinfo.objects.get(mobile=username)
        elif '@' in username:
            user_obj = models.Userinfo.objects.get(email=username)
        else:
            user_obj = models.Userinfo.objects.get(username=username)

        if not user_obj and user_obj.password == password:
            raise ValidationError('用户名或者密码错误')
        user = user_obj

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.context.update({'token': token, 'username': user.username})

        return attrs


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ['id','title', 'price', 'publishes','authors','publish','author']
        extra_kwargs = {
            'publishes': {'read_only': True},
            'authors': {'read_only':True},
            'publish': {'write_only': True},
            'author': {'write_only': True}
        }


class PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ['id','name','addr']
        extra_kwargs = {
            'id': {'read_only': True},

        }


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ['id','name', 'mobile']
        extra_kwargs = {
            'id': {'read_only': True},
        }
