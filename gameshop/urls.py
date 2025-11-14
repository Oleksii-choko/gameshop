from django.urls import path
from .views import *

urlpatterns = [
    path('',Index.as_view(), name='index'),
    path('shop/<slug:slug>',Shop.as_view(), name='shop_page'),
    path('game/<slug:slug>',Game.as_view(), name='game_page'),

]