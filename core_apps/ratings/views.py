from django.db import IntegrityError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from core_apps.ratings.exceptions import YouHaveAlreadyRated
from .models import Rating
from .serializers import RatingSerializer
from core_apps.articles.models import Article
from rest_framework.exceptions import ValidationError


class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    pagination_class = IsAuthenticated

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
            raise YouHaveAlreadyRated
