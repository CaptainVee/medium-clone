from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core_apps.common.models import TimeStampedModel

from .read_time_engine import ArticleReadTimeEngine

User = get_user_model()


class Article(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.CharField(verbose_name=_("Description"), max_length=500)
    body = models.TextField(verbose_name=_("Description"), max_length=500)
    banner_image = models.ImageField(
        verbose_name=_("Banner Image"), default="/profile_default.png"
    )
    claps = models.ManyToManyField(
        User, through="Clap", related_name="clapped_articles"
    )
    tags = TaggableManager()

    def __str__(self):
        return f"{self.author.first_name}'s articles"

    @property
    def estimated_reading_time(self):
        return ArticleReadTimeEngine.estimated_reading_time(self)

    def view_count(self):
        return self.article_views.count()

    def average_rating(self):
        ratings = self.ratings.all()

        if ratings.count() > 0:
            total_rating = sum(rating.rating for rating in ratings)
            average_rating = total_rating / ratings.count()
            return round(average_rating, 2)
        return None


class ArticleView(TimeStampedModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_views"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user_views"
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("viewer_IP"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Article View")
        verbose_name_plural = _("Article Views")
        unique_together = ("article", "user", "viewer_ip")

    def __str__(self) -> str:
        return f"{self.article.title} viewed by {self.user.get_short_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_view(cls, article, user, viewer_ip):
        view, _ = cls.objects.get_or_create(
            article=article, user=user, viewer_ip=viewer_ip
        )
        view.save()


class Clap(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["article", "user"]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.get_short_name} clapped {self.article.title}"
