
from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.Serializer):
      id = serializers.IntegerField(read_only=True)
      title = serializers.CharField(max_length=20, required=False)
      caption = serializers.CharField(max_length=256, required=True)
      content = serializers.CharField(max_length=100, required=True)

      def validate(self, data):
        if data['title'] is None:
            raise serializers.ValidationError("Title is required.")
        return data

      def create(self, validated_data):
        return Post.objects.create(**validated_data)

      def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.caption = validated_data.get('caption', instance.caption)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance





    
