from django.db import models


class Tag(models.Model):
    """Модель Тег"""
    name = models.CharField(
        'Название тега',
        max_length=200
    )
    color = models.CharField(
        'Код цвета',
        max_length=7
    )
    slug = models.SlugField(
        'Слаг тега',
        max_length=200
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name
