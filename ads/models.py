from django.db import models
from django.conf import settings


class Ad(models.Model):
    title = models.CharField('Название', max_length=200)
    price = models.IntegerField('Цена')
    description = models.TextField('Описание')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Объявление',
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.author} на {self.ad}'
