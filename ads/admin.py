from django.contrib import admin
from .models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text',)
