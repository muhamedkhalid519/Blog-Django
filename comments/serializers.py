from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'author',
            'author_name',
            'post',
            'is_deleted',
            'deleted_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'author',
            'author_name',
            'is_deleted',
            'deleted_at',
            'created_at',
            'updated_at',
        ]