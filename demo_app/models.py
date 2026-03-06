from django.db import models


class DemoModel(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name}(created:{self.created_at}|edited: {self.edited_at})'
    


