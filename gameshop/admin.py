from django.contrib import admin
from .models import *
# from django.utils.safestring import mark_safe\

admin.site.register(Category)


# prepopulated_fields = {'slug': 'title'}
