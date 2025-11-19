from django.urls import path
from .views import *

urlpatterns = [
    path('',Index.as_view(), name='index'),
    path('shop/',Shop.as_view(), name='shop_page'),
    path('contact_us/',contact_us, name='contact_us'),
    path('game_page/<slug:slug>/',GamePage.as_view(),name='game_page'),
]