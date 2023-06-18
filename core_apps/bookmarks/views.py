from uuid import UUID
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, NotFound
from core_apps.articles.models import Article
from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkCreateView(CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")

        if article_id:
            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError(
                    "An Article with the article id provided does not exist"
                )
        else:
            raise ValidationError("Article id is required")
        try:
            serializer.save(article=article, user=self.request.user)
        except IntegrityError:
            raise ValidationError("You have already bookmarked this article")


class BookmarkDestroyView(DestroyAPIView):
    queryset = Bookmark.objects.all()
    lookup_field = "article_id"
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        article_id = self.kwargs.get("article_id")

        try:
            UUID(str(article_id), version=4)
        except ValueError:
            raise ValidationError("Invalid article Id")

        try:
            bookmark = Bookmark.objects.get(user=user, article__id=article_id)
        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark don loss abi no be your own")
        return bookmark

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.user != user:
            raise ValidationError("You cannot delete a bookmark that isn't yours")
        instance.delete()
