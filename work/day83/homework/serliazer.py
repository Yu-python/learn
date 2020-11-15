from rest_framework import serializers
from . import models


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    publish = serializers.CharField()

    def update(self, instance, validated_data):
        print(instance)
        instance.title = validated_data.get('title')
        instance.price = validated_data.get('price')
        instance.publish = validated_data.get('publish')
        instance.save()
        return instance

    def create(self, validated_data):
        user_obj = models.Book.objects.create(**validated_data)
        return user_obj


