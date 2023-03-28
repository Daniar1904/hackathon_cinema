from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """Тег"""
    name = models.CharField("Имя", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Movie(models.Model):
    """Фильм"""
    image = models.ImageField(upload_to='movies/')
    title = models.CharField(max_length=250)
    tag = models.ManyToManyField(Tag, verbose_name='Теги')
    year = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.product}Liked by{self.author.email}'


class Favorites(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['author', 'movie']