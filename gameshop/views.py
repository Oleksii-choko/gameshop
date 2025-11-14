from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Category, Game


class Index(ListView):
    """Головна сторінка"""
    model = Game
    extra_context = {'title': 'Головна сторінка'}
    template_name = 'gameshop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вивід на сторінку додаткових елементів"""
        base_game = Game.objects.filter(is_published=True)

        context = super().get_context_data()  # Словарь
        context['categories'] = Category.objects.all()
        context['top_games'] = base_game.order_by('-watched')[:6]
        context['first_game'] = base_game.first()
        context['discount_game'] = base_game.order_by('?').filter(discount_percent__gt=0)[:4]
        return context


class Shop(ListView):
    """Сторінка магазину"""
    model = Game
    extra_context = {'title': 'Магазин'}
    context_object_name = 'games'
    template_name = 'gameshop/shop.html'

    def get_queryset(self):
        """Получение всех товаров определенной категории"""
        return ...



    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнительные элементы"""
        context = super().get_context_data()
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context