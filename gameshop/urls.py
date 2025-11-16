from django.urls import path
from .views import *

urlpatterns = [
    path('',Index.as_view(), name='index'),
    path('shop/',Shop.as_view(), name='shop_page'),
    path('shop/categories/<slug:slug>/', Shop.as_view(), name='shop_by_category'),

]