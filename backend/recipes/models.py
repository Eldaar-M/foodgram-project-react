from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

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

    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    ]

    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Юзернейм',
        max_length=MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ'
        )]
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
    role = models.CharField(
        'Роль пользователя',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=5,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=64)
    measurement_unit = models.CharField('Единица измерения', max_length=32)

    class Meta():
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Тег', unique=True, max_length=32)
    slug = models.SlugField(unique=True)
    color = models.CharField(
        max_length=16,
        unique=True,
    )

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
        verbose_name='Теги',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        through='RecipeTag'
    )
    cooking_time = models.PositiveIntegerField(
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


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                MIN_VALUE_VALID,
                message='Количество ингредиента не может быть нулевым')])


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
            )
        ]

    def __str__(self):
        return self.FOLLOW_PHRASE.format(
            user=self.user.username,
            author=self.author.username
        )


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
    )

    FAVOURITE_PHRASE = '{user} добавил в избранное рецепт {recipe}'

    class Meta:
        verbose_name = 'Избранное'
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


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Подписчик',
        help_text='Подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
    )
