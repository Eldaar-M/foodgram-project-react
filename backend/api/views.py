from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import mixins, viewsets, status, permissions, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (FavouriteSerializer,
                          IngredientSerializer,
                          RecipeSerializer,
                          RecipeFavouriteSerializer,
                          RecipePostSerializer,
                          SubscribeModelSerializer,
                          SubscribeUserSerializer,
                          ShoppingCartSerializer,
                          TagSerializer,
                          UserSerializer,
                          UserPostSerializer
                          )
from recipes.models import (Favourite,
                            Ingredient,
                            Recipe,
                            Subscribe,
                            ShoppingCart,
                            Tag,
                            )
from users.models import User


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def subscriptions(self, request):
        paginator = PageNumberPagination()
        authors = Subscribe.objects.filter(author__follower=request.user)
        result_page = paginator.paginate_queryset(authors, request)
        serializer = SubscribeUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            serializer = SubscribeModelSerializer(data={
                'user': request.user,
                'author': author}
            )
            serializer.is_valid()
            serializer.save(raise_exception=True)
            resonse_serializer = SubscribeUserSerializer(
                author,
                context={'request': request}
            )
            return Response(
                resonse_serializer.data, status=status.HTTP_201_CREATED
            )
        get_object_or_404(Subscribe,
                          user=request.user,
                          author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = RecipeFavouriteSerializer(recipe)
            if not Favourite.objects.filter(user=request.user,
                                            recipe=recipe).exists():
                Favourite.objects.create(user=request.user,
                                         recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Рецепт уже есть в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not Favourite.objects.filter(user=request.user,
                                          recipe=recipe).exists():
            get_object_or_404(Favourite,
                              user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепта нет в избранном'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(ShoppingCart, pk=pk)
        if request.method == 'POST':
            serializer = RecipeFavouriteSerializer(recipe)
            if not ShoppingCart.objects.filter(user=request.user,
                                               recipe=recipe).exists():
                ShoppingCart.objects.create(user=request.user,
                                            recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Рецепт уже есть в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not ShoppingCart.objects.filter(user=request.user,
                                             recipe=recipe).exists():
            get_object_or_404(ShoppingCart,
                              user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепта нет в избранном'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def download_shopping_cart(self, request, pk=None):
        pass

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
