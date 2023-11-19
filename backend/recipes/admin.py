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


class UserAdmin(UserAdmin):
    """Класс настройки раздела пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'follower_count',
        'following_count',
        'recipes_count'
    )

    search_fields = ('username',)

    @admin.display(description='Подписчики')
    def follower_count(self, user):
        return user.follower.count()

    @admin.display(description='Подписки')
    def following_count(self, user):
        return user.following.count()

    @admin.display(description='Рецепты')
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
            f'<span style="background-color:{tag.color}; '
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
        'get_image',
        'get_ingredients',
        'get_tags',
        'pub_date',
        'in_favorite'
    )

    inlines = [
        RecipeIngredientInline,
    ]

    list_filter = ('author', 'tags')
    search_fields = ('author', 'name')

    @admin.display(description='Картинка')
    def get_image(self, recipe):
        return mark_safe(f'<img src={recipe.image.url} width="50" height="60"')

    @admin.display(description='Теги')
    def get_tags(self, recipe):
        tags = recipe.tags.all()
        tag_list = ''
        for tag in tags:
            tag_list += '{}'.format(''.join(tag.name))
        return tag_list

    @admin.display(description='Продукты')
    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.all()
        ingredient_list = ''
        for ingredient in ingredients:
            ingredient_list += '{}'.format(''.join(ingredient.name))
        return ingredient_list

    @admin.display(description='В избранном')
    def in_favorite(self, recipe):
        return recipe.favourites.all().count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe',
        'measurement_unit'
    )

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


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
