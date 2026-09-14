from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet #, ReviewViewSet

router = DefaultRouter()
router.register('ads', AdViewSet, basename='ad')
#router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]