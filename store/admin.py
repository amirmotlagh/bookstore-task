from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from store.models import CustomUser, Book


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'author_pseudonym',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'author_pseudonym',)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('author_pseudonym', 'is_staff', 'is_active',)
    list_filter = ('author_pseudonym', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'author_pseudonym', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'author_pseudonym', 'password1', 'password2', 'is_staff',
                       'is_active')}
        ),
    )
    search_fields = ('author_pseudonym',)
    ordering = ('author_pseudonym',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)
