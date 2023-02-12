from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = None
    password2 = None

    class Meta:
        model = User
        fields = ('address', 'username')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('address', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('address', 'username', 'is_admin')
    list_filter = ('is_admin', )
    search_fields = ('address', 'username')
    ordering = ('address', 'username')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)