from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages


from .models import Category, Game

class Index(ListView):
    """Головна сторінка"""
    model = Game
    # context_object_name = 'categories'
    extra_context = {'title': 'Головна сторінка'}
    template_name = 'gameshop/index.html'

    # def get_queryset(self):
    #     """Вывод родительских категорий"""
    #     return ...

    # def get_context_data(self, *, object_list=None, **kwargs):
    # """Вывод на страничку дополнительных элементов"""
    # context = super().get_context_data()  # Словарь
    # context['top_product'] = Product.objects.order_by('-watched')[:3]
    # return context