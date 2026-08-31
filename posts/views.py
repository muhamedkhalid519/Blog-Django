from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from .models import Post
from .serializers import PostSerializer
from users.permissions import IsOwnerOrAdmin


class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(is_deleted=False)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]

        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Post.objects.get(
                pk=pk,
                is_deleted=False
            )
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post)

        return Response(serializer.data)

    def patch(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, post)

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, post)

        post.is_deleted = True
        post.save()

        return Response(
            {'message': 'Post deleted successfully'},
            status=status.HTTP_200_OK
        )


def home(request):
    return render(request, 'blog/home.html')

def post_detail(request, post_id):
    return render(request, 'blog/post_detail.html')

def create_post(request):
    return render(request, 'blog/create_post.html')

def edit_post(request, post_id):
    return render(request, 'blog/edit_post.html')