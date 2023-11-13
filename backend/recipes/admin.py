from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import (
    Favourite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
    RecipeTag
)

User = get_user_model()

LIST_PER_PAGE = 6


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс настройки раздела пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = ('username', 'email')
    list_per_page = LIST_PER_PAGE
    search_fields = ('username',)


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )

    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):

    model = RecipeIngredient
    min_num = 1


class RecipeTagInLine(admin.TabularInline):

    model = RecipeTag
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'cooking_time',
        'image',
        'pub_date',
        'count_favorite',
    )
    inlines = [
        RecipeIngredientInline,
        RecipeTagInLine,
    ]

    list_filter = ('author', 'name', 'tags')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author', 'name')

    def count_favorite(self, object):
        return object.favourites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe'
    )
    list_per_page = LIST_PER_PAGE


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = LIST_PER_PAGE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = LIST_PER_PAGE
