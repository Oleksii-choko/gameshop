from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Category, Game, Genre, Platform
from .forms import GameFilterForm


class Index(ListView):
    """Головна сторінка"""
    model = Game
    extra_context = {'title': 'Головна сторінка'}
    template_name = 'gameshop/index.html'

    def get_queryset(self):
        """ Основний список ігор для головної"""
        return (
            Game.objects
            .filter(is_published=True)
            .select_related('category')
            .prefetch_related('platforms', 'genres')
            .order_by('-created_at'))

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вивід на сторінку додаткових елементів"""
        context = super().get_context_data()  # Словарь
        base_game = self.get_queryset()

        context['categories'] = Category.objects.only('id', 'title', 'slug', 'image')
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
    paginate_by = 6

    def get_queryset(self):
        qs = (Game.objects.filter(is_published=True)
              .select_related("category")
              .prefetch_related("platforms", "genres"))
        form = self.get_form()
        if form.is_valid():
            cats = form.cleaned_data['category']  # QuerySet<Category>
            plats = form.cleaned_data['platform']  # QuerySet<Platform>
            gens = form.cleaned_data['genre']  # QuerySet<Genres>
            pmin = form.cleaned_data['price_min']  # Decimal | None
            pmax = form.cleaned_data['price_max']  # Decimal | None

            if cats:
                qs = qs.filter(category__in=cats)

            if pmin is not None:
                qs = qs.filter(price__gte=pmin)
            if pmax is not None:
                qs = qs.filter(price__lte=pmax)

            # M2M за замовчуванням: OR (будь-яка з обраних)
            if plats:
                if form.cleaned_data.get('require_all_platforms'):
                    for p in plats:
                        qs = qs.filter(platforms=p)
                else:
                    qs = qs.filter(platforms__in=plats)

            if gens:
                if form.cleaned_data.get('require_all_genres'):
                    for g in gens:
                        qs = qs.filter(genres=g)
                else:
                    qs = qs.filter(genres__in=gens)
        return qs.distinct().order_by("-created_at")

    def get_form(self):
        initial = {}
        if slug := self.kwargs.get("slug"):
            initial["category"] = [slug]
        return GameFilterForm(self.request.GET or None, initial=initial)



    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнительные элементы"""
        ctx = super().get_context_data()
        ctx['form'] = getattr(self, 'form', self.get_form())
        ctx['categories'] = Category.objects.only('id','title','slug')
        ctx['genres'] = Genre.objects.only('id','title')
        ctx['platforms'] = Platform.objects.only('id','title')
        return ctx