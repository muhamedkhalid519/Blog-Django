from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'author',
            'is_deleted',
            'deleted_at',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'author',
            'is_deleted',
            'deleted_at',
            'created_at',
            'updated_at'
        ]

        