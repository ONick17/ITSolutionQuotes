from django.db import models
from django.core.exceptions import ValidationError


class Quote(models.Model):
    id = models.BigAutoField(primary_key=True)
    # text = models.TextField(unique=True, blank=False, verbose_name="Цитата")
    text = models.CharField(
        max_length=1000,
        unique=True,
        verbose_name="Цитата"
    )
    source = models.CharField(max_length=255, blank=False, verbose_name="Источник")
    weight = models.PositiveIntegerField(default=1, verbose_name="Вес цитаты")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        if Quote.objects.filter(source=self.source).count() >= 3 and not self.pk:
            raise ValidationError("Нельзя добавить больше 3 цитат из одного источника.")

    def __str__(self):
        return f"{self.text} (Источник: \"{self.source}\")"
