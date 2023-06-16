import logging
from django.http import Http404
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import Article, ArticleView
from .pagination import ArticlePagination
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .serializers import ArticleSerializer
from .filters import ArticleFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser


User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = ArticlePagination
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "updated_at"]
    renderer_classes = [ArticlesJSONRenderer]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(
            f'article {serializer.data.get("title")} created by {self.request.user.get_short_name}'
        )


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    renderer_classes = [ArticleJSONRenderer]
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        if "banner_image" in self.request.FILES:
            if (
                instance.banner_image
                and instance.banner_image.name != "/profile_default.png"
            ):
                default_storage.delete(instance.banner_image.path)
            instance.banner_image = self.request.FILES["banner_image"]
            instance.save()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        viewer_ip = request.META.get("REMOTE_ADDR", None)
        ArticleView.record_view(
            article=instance, user=request.user, viewer_ip=viewer_ip
        )

        return Response(serializer.data)
