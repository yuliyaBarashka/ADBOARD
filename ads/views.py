from rest_framework import viewsets, permissions
from .models import Ad, Review
from .serializers import AdSerializer, AdDetailSerializer
# from .permissions import IsAuthorOrAdminOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
   # permission_classes = [IsAuthorOrAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


