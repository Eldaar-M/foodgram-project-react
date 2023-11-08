from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

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
