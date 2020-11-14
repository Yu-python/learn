from rest_framework import serializers

from . import models


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
    user_type = serializers.CharField(source='get_user_type_display')


class PublishModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publish
        fields = '__all__'


class BooksModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
    publish = serializers.SerializerMethodField()

    def get_publish(self,instance):
        return {"id":instance.publish.pk,'name':instance.publish.name,'addr':instance.publish.addr}

    # publish = PublishModelSerializer()