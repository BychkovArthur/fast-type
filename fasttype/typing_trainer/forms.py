from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import *


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Повтор пароля"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email")


class UpdateSettingsForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["show_wpm"].widget.attrs.update(
            {"class": "form-check-input checkbox-scale", "role": "switch", "id": "qwe"}
        )
        self.fields["show_time"].widget.attrs.update(
            {"class": "form-check-input checkbox-scale", "role": "switch"}
        )
        self.fields["show_percent_done"].widget.attrs.update(
            {"class": "form-check-input checkbox-scale", "role": "switch"}
        )
        self.fields["show_symbols_count"].widget.attrs.update(
            {"class": "form-check-input checkbox-scale", "role": "switch"}
        )
        self.fields["current_theme"].widget.attrs.update(
            {"class": "form-select form-select-lg my-3"}
        )
        self.fields["current_text"].widget.attrs.update(
            {"class": "form-select form-select-lg my-3"}
        )
        self.fields["current_text"].empty_label = "Не выбран"
        self.fields["current_author"].widget.attrs.update(
            {"class": "form-select form-select-lg my-3"}
        )
        self.fields["current_author"].empty_label = "Не выбран"
        self.fields["current_category"].widget.attrs.update(
            {"class": "form-select form-select-lg my-3"}
        )
        self.fields["current_category"].empty_label = "Не выбрана"

    class Meta:
        model = Settings
        fields = (
            "show_wpm",
            "show_percent_done",
            "show_time",
            "show_symbols_count",
            "current_text",
            "current_author",
            "current_category",
            "current_theme",
        )


class AddTextForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Заголовок"}
        )
        self.fields["text"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Текст"}
        )
        self.fields["language"].widget.attrs.update({"class": "form-select"})
        self.fields["language"].empty_label = "Не выбран"
        self.fields["author"].widget.attrs.update({"class": "form-select"})
        self.fields["author"].empty_label = "Не выбран"
        self.fields["category"].widget.attrs.update({"class": "form-select"})
        self.fields["category"].empty_label = "Не выбрана"

    class Meta:
        model = Text
        fields = (
            "title",
            "text",
            "author",
            "category",
            "language",
        )


class AddAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя"}
        )

    class Meta:
        model = Author
        fields = ("name",)


class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )

    class Meta:
        model = TextCategory
        fields = ("title",)
