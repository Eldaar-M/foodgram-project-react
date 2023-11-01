from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import mixins, viewsets, status, permissions, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filter
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters import rest_framework as rest_filter
from api.permissions import (IsAdminRoleOrIsStaff,
                             IsAuthorOrAdminOrModerator,
                             ReadOnlyOrAdmin, )
from .serializers import (FavouriteSerializer,
                          RecipeSerializer,
                          SubscribeSerializer,
                          ShoppingCartSerializer,
                          IngredientSerializer)
from api.filters import TitleFilter
from recipes.models import (Favourite,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            Subscribe,
                            ShoppingCart,
                            Tag,
                            )
from users.models import User


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer