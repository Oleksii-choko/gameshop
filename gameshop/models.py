from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):



    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
