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

    def get_queryset(self):
        """Вивід категорій"""
        categories = Category.objects.all()
        return categories

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вывод на страничку дополнительных элементов"""
        base_game = Game.objects.filter(is_published=True)

        context = super().get_context_data()  # Словарь
        context['categories'] = Category.objects.all()
        context['top_games'] = base_game.order_by('-watched')[:6]
        context['first_game'] = base_game.order_by('?').first()
        context['discount_game'] = Game.objects.order_by('?').filter(discount_percent__gt=0, is_published=True)[:4]
        return context