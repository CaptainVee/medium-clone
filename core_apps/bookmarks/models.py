from django.db import models
from django.contrib.auth import get_user_model
from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedModel


User = get_user_model()


class Bookmark(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    article = models.ForeignKey(
        Article, related_name="bookmarks", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["user", "article"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.get_short_name} bookmarked {self.article.title}"
