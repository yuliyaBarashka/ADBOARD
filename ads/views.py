from rest_framework import viewsets, permissions
from .models import Ad, Review
from .serializers import AdSerializer, AdDetailSerializer, ReviewSerializer
from .permissions import IsAuthorOrAdminOrReadOnly
from .filters import AdFilter
from .paginators import AdPagination
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(summary='Список объявлений', tags=['Ads']),
    create=extend_schema(summary='Создать объявление', tags=['Ads']),
    retrieve=extend_schema(summary='Получить объявление', tags=['Ads']),
    update=extend_schema(summary='Обновить объявление', tags=['Ads']),
    partial_update=extend_schema(summary='Частично обновить объявление', tags=['Ads']),
    destroy=extend_schema(summary='Удалить объявление', tags=['Ads']),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filterset_class = AdFilter
    pagination_class = AdPagination
    search_fields = ['title']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        ad_id = self.request.query_params.get('ad')
        if ad_id:
            queryset = queryset.filter(ad_id=ad_id)
        return queryset

