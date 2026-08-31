from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta: 
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'author',
            'author_username',
            'is_deleted',
            'deleted_at',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'slug',
            'author',
            'is_deleted',
            'deleted_at',
            'created_at',
            'updated_at'
        ]

        