from django.contrib import admin

# Register your models here.
#from django.db import models
from .models import User

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'registration_date']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')
    
    def clean_password(self):
        return self.initial["password"]
        

class PasswordChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Old Password')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password',)

    def clean_password(self):
        return self.initial["password"]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords dont match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = PasswordChangeForm
    # list_display = ('username', 'email', 'first_name', 'last_name', 'registration_date', 'is_admin', 'is_superuser',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'password')}),
        ('Personal info', {'fields':('email','registration_date',)}),
        ('Permissions', {'fields': ('is_admin','is_active','is_superuser',)}),
    )
    readonly_fields = ('registration_date',)
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('username', 'first_name', 'last_name','email','registration_date', 'password1','password2')}
        ),
    )
    search_fields = ('first_name', 'last_name','email','username', 'id')
    ordering = ('username',)
    filter_horizontal = ()
    filter_vertical = ()

    def has_add_permission(self, request):
        has_class_permission = super(UserAdmin, self).has_add_permission(request)
        if not has_class_permission:
            return False
        if request.user is not None and not request.user.is_superuser:
            return False
        return True
    
    """def has_view_permission(self, request, obj=None):
        has_class_permission = super(UserAdmin, self).has_view_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user != obj.username:
            return False
        return True"""

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(UserAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user != obj.username:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(UserAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user)

    """def get_fields(self, request):
        if request.user.is_superuser:
            return ['username', 'email', 'first_name', 'last_name', 'registration_date', 'is_admin', 'is_superuser',]
        return ['username', 'email', 'first_name', 'last_name', 'registration_date'] """

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
