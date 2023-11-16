from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import (
    Favourite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)

User = get_user_model()

LIST_PER_PAGE = 6


class UserAdmin(UserAdmin):
    """Класс настройки раздела пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'follower_count',
        'following_count',
        'recipes_count'
    )
    list_filter = ('username', 'email')
    list_per_page = LIST_PER_PAGE
    search_fields = ('username',)

    @admin.display(description='Число подписчиков')
    def follower_count(self, user):
        return user.follower.count()

    @admin.display(description='Число подписок')
    def following_count(self, user):
        return user.following.count()

    @admin.display(description='Число рецептов')
    def recipes_count(self, user):
        return user.recipes.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
        'preview'
    )

    @admin.display(description='Предпросмотр')
    def preview(self, tag):
        return mark_safe(
            f'<span style="color:{tag.color}; '
            f'width=20px; height=20px;">{tag.name}</span>'
        )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )

    list_filter = ('measurement_unit',)
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
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
    )

    inlines = [
        RecipeIngredientInline,
    ]

    list_filter = ('author', 'name', 'tags')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author', 'name')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe',
        'measurement_unit'
    )
    list_per_page = LIST_PER_PAGE

    @admin.display(description='Единица измерения')
    def measurement_unit(self, instance):
        return instance.ingredient.measurement_unit


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


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
