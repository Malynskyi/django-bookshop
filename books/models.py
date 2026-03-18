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
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class PublishedBookManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_available=True)
    
    def expensive(self):
        return self.filter(price__gt=100)
    
    def by_author(self, author_lname):
        return self.filter(author__last_name__icontains=author_lname)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category Name')
    slug = models.SlugField(unique=True, verbose_name='URL Slug')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Book title',  default=0)
    published_at = models.DateField(verbose_name='Release date', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price',  default=0)
    objects = models.Manager()
    published = PublishedBookManager()
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    stock = models.PositiveIntegerField(default=0, verbose_name='In Stock')
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        related_name='books',
        verbose_name='Category'
    )

    def __str__(self) -> str:
        return f'{self.title}{self.published_at}'
    
    @property
    def is_on_market(self):
        return all([self.is_available, self.author])
    
    def clean(self) -> None:
        return super().clean()
    

class Meeting(models.Model):
    title = models.CharField(max_length=150)
    schedule = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.title} at {self.schedule.strftime('%Y-%m-%dT%H:%M')}'
    
    def clean(self):
        current_datetime = timezone.now()
        if self.schedule < current_datetime:
            raise ValidationError({
                'schedule': 'Can\'t assign date before current'
            })
        

class Publisher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='publisher',
        verbose_name='User'
    )


    contact_phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Phone contact'
    )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.contact_phone}'