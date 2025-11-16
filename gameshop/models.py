from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

class Language(models.Model):
    title = models.CharField(max_length=255, verbose_name='Мова озвучки', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мова'
        verbose_name_plural = 'Мови'


class Platform(models.Model):
    title = models.CharField(max_length=255, verbose_name='Платформа', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформи'

class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name='Жанр', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'

class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тег', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва категорії')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Зображення')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    def get_absolute_url(self):
        """Посилання на категорію"""
        return reverse('shop_by_category', kwargs={'slug': self.slug})

    def get_category_photo(self):  # щоб діставав фото категорій
        if self.image:
            return self.image.url
        else:
            return 'https://placehold.co/600x400/EEEEEE/222222?text=No+Image'

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name='Відеогра')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    discount_percent = models.PositiveSmallIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Знижка'
    )
    stock = models.PositiveIntegerField(default=100, verbose_name='Кількість')
    genres = models.ManyToManyField(Genre, blank=True, related_name='games', verbose_name='Жанр')
    tags = models.ManyToManyField(Tag, blank=True, related_name='games', verbose_name='Тег')
    platforms = models.ManyToManyField(Platform, blank=True, related_name='games', verbose_name='Платформа')
    languages_supported = models.ManyToManyField(Language, blank=True, related_name='games', verbose_name='Мова')
    publisher = models.CharField(max_length=255, verbose_name='Видавництво')
    image = models.ImageField(upload_to='product/', null=True, blank=True, verbose_name='Зображення')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    watched = models.PositiveIntegerField(default=0, verbose_name='Перегляди')
    description = models.TextField(default='Тут скоро зʼявиться ваш опис...', verbose_name='Опис гри')
    info = models.TextField(default='Додаткова інформація про продукт', verbose_name='Інформація про гру')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категорія', related_name='games')
    slug = models.SlugField(unique=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name='Опублікований')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Гра: pk={self.pk}, title={self.title}, price={self.price}'

    def get_absolute_url(self):
        """Посилання на гру"""
        return reverse('game_page', kwargs={'slug': self.slug})

    def get_game_photo(self):  # щоб діставав фото категорій
        if self.image:
            return self.image.url
        else:
            return 'https://placehold.co/600x400/EEEEEE/222222?text=No+Image'

    class Meta:
        verbose_name = 'Відеогра'
        verbose_name_plural = 'Відеоігри'


# model Coupon
# code (унікальний, кеш-інсенситив).
# 	•	discount_type: percent або fixed.
# 	•	value: число (для percent — 0..100, для fixed — в тій же валюті, що price).
# 	•	valid_from, valid_to, is_active.
# 	•	min_order_amount (опційно).
# 	•	usage_limit, usage_limit_per_user (опційно).
# 	•	Сфери застосування (одне або кілька): applies_to_all, або зв’язки на categories/products/tags/platforms/publisher.
# 	•	Політика складання (stacking):
# 	•	include_sale_items (bool): чи діє на товари вже зі знижкою.
# 	•	stack_policy: stack (поверх акцій), replace (замінює знижку товару, якщо вигідніше), forbid (лише на несофтнені товари).
# 	•	(опційно) max_discount_amount — верхня межа вигоди по купону.
