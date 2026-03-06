# from django.db import models
# # from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# #этот метод возвращает актуальный класс модели пользователя
# User = get_user_model()


# class Book(models.Model):
#     name = models.CharField(max_length=150, verbose_name='Book title')
#     published_at = models.DateField(verbose_name='Release date')
#     author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

#     def __str__(self) -> str:
#         return f'{self.name}({self.published_at}) - {self.author}'
    

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category Name')
    slug = models.SlugField(unique=True, verbose_name='URL Slug')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Book title',  default=0)
    author = models.CharField(max_length=100, verbose_name='Author')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price',  default=0)
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    stock = models.PositiveIntegerField(default=0, verbose_name='In Stock')

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        related_name='books',
        verbose_name='Category'
    )

    def __str__(self):
        return self.title