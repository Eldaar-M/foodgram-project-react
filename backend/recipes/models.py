from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import validate_username

MAX_LENGTH = 150

MIN_VALUE_VALID = 1


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Никнейм',
        max_length=MAX_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH
    )
    password = models.CharField(
        'Пароль',
        max_length=MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    name = models.CharField('Название продукта', max_length=64)
    measurement_unit = models.CharField('Единица измерения', max_length=32)

    class Meta():
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField('Тег', unique=True, max_length=32)
    slug = models.SlugField(unique=True)
    color = ColorField(default='#FF0000',
                       max_length=7,
                       unique=True,
                       verbose_name='Цвет в HEX')

    class Meta():
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор этого рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        'Картинка',
        help_text='Картинка рецепта',
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField(
        'Текстовое описание',
        help_text='Напишите описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Продукты',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                MIN_VALUE_VALID, message='Время приготовления от 1 минуты'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta():
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Мера',
        validators=[
            MinValueValidator(
                MIN_VALUE_VALID,
                message='Количество продуктов не может быть нулевым')])

    class Meta:
        verbose_name = 'Продукт в рецепте'
        verbose_name_plural = 'Продукты в рецепте'

    def ingredients_shopping_cart(self, request):
        return RecipeIngredient.objects.filter(
            recipe__shopping_carts__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=models.Sum('amount'))


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор'
    )

    FOLLOW_PHRASE = '{user} подписался на {author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name="user_cannot_follow_himself",
            ),
        ]

    def __str__(self):
        return self.FOLLOW_PHRASE.format(
            user=self.user.username,
            author=self.author.username
        )


class UserRecipeModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        ordering = ('recipe',)


class Favourite(UserRecipeModel):

    FAVOURITE_PHRASE = '{user} добавил в избранное рецепт {recipe}'

    class Meta(UserRecipeModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        default_related_name = 'favourites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourites'
            )
        ]

    def __str__(self):
        return self.FAVOURITE_PHRASE.format(
            user=self.user.username,
            author=self.recipe.name
        )


class ShoppingCart(UserRecipeModel):

    FAVOURITE_PHRASE = '{user} добавил {recipe} в корзину'

    class Meta(UserRecipeModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_carts'

    def __str__(self):
        return self.FAVOURITE_PHRASE.format(
            user=self.user.username,
            author=self.recipe.name
        )
