from rest_framework import serializers
from .models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'description', 'author', 'created_at')
        read_only_fields = ('author', 'created_at')


class AdDetailSerializer(AdSerializer):
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta(AdSerializer.Meta):
        fields = AdSerializer.Meta.fields + ('reviews_count',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'ad', 'created_at')
        read_only_fields = ('author', 'created_at')
