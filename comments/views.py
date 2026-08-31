from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from users.permissions import IsOwnerOrAdmin

# Create your views here.

class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.filter(is_deleted=False)
        serializer = CommentSerializer(comments)
        return Response(serializer.data)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated]


    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk, is_deleted=False)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {'error': 'Comment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {'error': 'Comment Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {'error': 'Comment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permission(request, comment)
        comment.is_deleted = True
        comment.save()
        return Response(
            {'message': 'Comment Deleted Successfully'},
            status=status.HTTP_200_OK
        )