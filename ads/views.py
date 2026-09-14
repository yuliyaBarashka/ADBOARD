from rest_framework import viewsets, permissions
from .models import Ad, Review
from .serializers import AdSerializer, AdDetailSerializer, ReviewSerializer
from .permissions import IsAuthorOrAdminOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]

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

