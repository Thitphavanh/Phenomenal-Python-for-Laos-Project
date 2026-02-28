from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class CustomUserCreationForm(UserCreationForm):
    """Custom registration form with additional fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary transition-all',
            'placeholder': _('ອີເມວຂອງທ່ານ')
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary transition-all',
            'placeholder': _('ຊື່ຜູ້ໃຊ້')
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary transition-all',
            'placeholder': _('ລະຫັດຜ່ານ')
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary transition-all',
            'placeholder': _('ຢືນຢັນລະຫັດຜ່ານ')
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with styled widgets"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary transition-all',
            'placeholder': _('ຊື່ຜູ້ໃຊ້')
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary transition-all',
            'placeholder': _('ລະຫັດຜ່ານ')
        })
    )