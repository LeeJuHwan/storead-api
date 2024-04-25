from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from .models import Article, Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        return Comment.objects.filter(article__id=article_id, parent_comment=None)

    def perform_create(self, serializer):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        serializer.save(user=user, article=article)


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        user = self.request.user
        comment = self.get_object()

        if user != comment.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        comment = self.get_object()

        if user != comment.user:
            raise PermissionDenied(
                "You do not have permission to delete this comment."
            )
        instance.delete()
