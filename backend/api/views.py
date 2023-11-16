from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.viewsets import ModelViewSet


from .filters import IngredientSearchFilter, RecipeFilter
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeAddSerializer,
    RecipeCreateSerializer,
    SubscribeModelSerializer,
    SubscribeUserSerializer,
    TagSerializer,
    UserSerializer,
)
from .send_file import sending
from .permissions import AuthorOrReadOnly, AdminOrReadOnly
from .pagination import Paginator
from recipes.models import (
    Favourite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Subscribe,
    ShoppingCart,
    Tag,
)

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrReadOnly,)

    @action(methods=['get'],
            detail=False)
    def subscriptions(self, request):
        paginator = Paginator()
        authors = User.objects.filter(following__user=request.user)
        # author = request.user.follower.all()
        result_page = paginator.paginate_queryset(authors, request)
        serializer = SubscribeUserSerializer(
            result_page,
            context={'request': request},
            many=True
        )
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscribeModelSerializer(data={
                'user': request.user.id,
                'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_serializer = SubscribeUserSerializer(
                author,
                context={'request': request}
            )
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )
        get_object_or_404(Subscribe,
                          user=request.user,
                          author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        return RecipeCreateSerializer

    def shopping_cart_favorite(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = RecipeAddSerializer(recipe)
            model.objects.get_or_create(user=request.user, recipe=recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            get_object_or_404(model,
                              user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        return self.shopping_cart_favorite(Favourite, request, pk)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        return self.shopping_cart_favorite(ShoppingCart, request, pk)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.ingredients_shopping_cart(
            self,
            request=request
        )
        return FileResponse(
            sending(ingredients),
            content_type='text/plain',
            filename='products.txt'
        )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientSearchFilter
    search_fields = ('^name', )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
