from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .utils import DataMixin, queryset_to_dict, get_model_by_statistic_type
from .forms import *
from .models import *
from .utils import update_statistic_by, update_stat_if_exists, get_slug_prop_model
import ast
from django.db.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import json


def choose_random(request, type):
    """Меняет настройку одну из настроек пользователя:
    1. Текущий текст
    2. Текущий автор
    3. Текущая категория
    """
    if type == "text":
        model = Text
        attr = "current_text"

    elif type == "category":
        model = TextCategory
        attr = "current_category"

    elif type == "author":
        model = Author
        attr = "current_author"

    else:
        raise Http404()

    user_settings = Settings.objects.get(pk=request.user.pk)
    setattr(user_settings, attr, random.choice(model.objects.all()))
    user_settings.save()
    return redirect(user_settings.get_absolute_url())


def index(request):
    context = {
        "title": "Главная страница",
        "menu_selected": "index",
    }

    if request.user.is_authenticated:
        user_settings = Settings.objects.get(pk=request.user.pk)
        context["user_settings"] = user_settings

        # Выбран текст. Остальное - без разницы
        if user_settings.current_text:
            text_object = user_settings.current_text
            text_category = text_object.category
            text_author = text_object.author
        # Выбраны и категория и автор, а текст не выбран
        elif user_settings.current_category and user_settings.current_author:
            # Если существует хотябы один текст с указанным автором и указанной категорией, выбираем случайный из этих
            if Text.objects.filter(
                category=user_settings.current_category,
                author=user_settings.current_author,
            ).exists():
                text_object = random.choice(
                    Text.objects.filter(
                        category=user_settings.current_category,
                        author=user_settings.current_author,
                    )
                )
                text_category = user_settings.current_category
                text_author = user_settings.current_author
            # Если же ни одного текста нет, выбираем случайный из всех текстов
            else:
                text_object = random.choice(Text.objects.all())
                text_category = text_object.category
                text_author = text_object.author
        # Выбрана только категория
        elif user_settings.current_category:
            if Text.objects.filter(category=user_settings.current_category).exists():
                text_object = random.choice(
                    Text.objects.filter(category=user_settings.current_category)
                )
                text_category = user_settings.current_category
                text_author = text_object.author
            else:
                text_object = random.choice(Text.objects.all())
                text_category = text_object.category
                text_author = text_object.author
        # Выбран только автор
        elif user_settings.current_author:
            if Text.objects.filter(author=user_settings.current_author).exists():
                text_object = random.choice(
                    Text.objects.filter(author=user_settings.current_author)
                )
                text_category = text_object.category
                text_author = user_settings.current_author
            else:
                text_object = random.choice(Text.objects.all())
                text_category = text_object.category
                text_author = text_object.author
        # Ничего не выбрано
        else:
            text_object = random.choice(Text.objects.all())
            text_category = text_object.category
            text_author = text_object.author
    else:
        context["user_settings"] = None
        text_object = random.choice(Text.objects.all())
        text_category = text_object.category
        text_author = text_object.author

    context["text_object"] = text_object
    context["text_category"] = text_category
    context["text_author"] = text_author

    # Добавляю в шаблон цвет правильной буквы
    # цвет ошибочной буквы и цвет буквы по умолчанию
    if context["user_settings"]:
        current_theme = context["user_settings"].current_theme
    else:
        current_theme = Theme.objects.get(pk=1)
    theme_colors = json.loads(current_theme.css)
    context["fontColor"] = theme_colors["fontColor"]
    context["correctLetterColor"] = theme_colors["correctLetterColor"]
    context["wrongLetterColor"] = theme_colors["wrongLetterColor"]

    return render(
        request=request,
        template_name="typing_trainer/index.html",
        context=context,
    )


class Registration(DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = "typing_trainer/post_forms.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Регистрация",
            "button_text": "Зарегистрироваться",
            "menu_selected": "registration",
        }
        return self.get_context(context=context, additional_context=additional_context)

    def form_valid(self, form):
        user = form.save()
        Settings.objects.create(user=user)
        login(self.request, user)
        return redirect("index")


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = "typing_trainer/post_forms.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Вход",
            "button_text": "Войти",
            "menu_selected": "login",
        }
        return self.get_context(context=context, additional_context=additional_context)

    def get_success_url(self):
        return reverse_lazy("index")


def logout_user(request):
    logout(request)
    return redirect("login", permanent=True)


def add_statistic(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = ast.literal_eval(request.body.decode("utf-8"))
            user = request.user
            text = Text.objects.get(pk=data["text"])

            # Обновление общей статистики
            if Statistics.objects.filter(pk=user.pk).exists():
                stat = Statistics.objects.get(pk=user)
                stat.last_text = text
                update_stat_if_exists(stat, data)
            else:
                wpm = int(data["wpm"])
                acc = float(data["acc"])
                Statistics.objects.create(
                    user=user,
                    last_text=text,
                    average_wpm=wpm,
                    best_wpm=wpm,
                    count_typed=1,
                    average_accuracy=acc,
                )

            # Преобразую pk в объект, чтобы в функции можно
            # было обращаться к этому объекту, как к fk
            user_stat_obj = Statistics.objects.get(user=user)

            data["text"] = Text.objects.get(pk=data["text"])
            update_statistic_by("text", TextStatistics, data, user_stat_obj)

            # Если у меня для текста не указан
            # автор или категория, в шаблоне будет
            # пустая строк, и через json придет
            # так же пустая строка
            if data["author"]:
                data["author"] = Author.objects.get(pk=data["author"])
                update_statistic_by("author", AuthorStatistics, data, user_stat_obj)

            if data["category"]:
                data["category"] = TextCategory.objects.get(pk=data["category"])
                update_statistic_by("category", CategoryStatistics, data, user_stat_obj)

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "401"})


class UserSettings(DataMixin, UpdateView):
    model = Settings
    form_class = UpdateSettingsForm
    template_name = "typing_trainer/settings.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        # Запрещаем пользователям смотреть чужие настройки
        if self.kwargs["pk"] != self.request.user.pk:
            raise PermissionDenied()
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Настройки",
            "menu_selected": "settings",
        }
        return self.get_context(context=context, additional_context=additional_context)


class UserStatistics(DataMixin, ListView):
    template_name = "typing_trainer/stat_and_leaderboard.html"
    context_object_name = "statistics"
    additional_context = {
        "title": "Статистика",
        "menu_selected": "statistics",
    }

    def get_queryset(self):
        model = get_model_by_statistic_type(self.kwargs, self.additional_context)
        self.additional_context["username"] = self.request.user.username
        if self.kwargs["statistic_type"] == "general":
            return model.objects.filter(user=self.kwargs["pk"])
        return model.objects.filter(user_statistic=self.kwargs["pk"]).select_related(self.additional_context["stat_selected"])

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return self.get_context(
            context=context, additional_context=self.additional_context
        )


class Leaderboard(DataMixin, ListView):
    template_name = "typing_trainer/stat_and_leaderboard.html"
    context_object_name = "statistics"
    additional_context = {
        "title": "Таблица лидеров",
        "menu_selected": "leaderboard",
    }

    def get_queryset(self):
        model = get_model_by_statistic_type(self.kwargs, self.additional_context)
        if self.kwargs["statistic_type"] == "general":
            return model.objects.all().select_related("user").prefetch_related("last_text")
        else:
            return model.objects.all().select_related("user_statistic").prefetch_related("user_statistic__user", self.additional_context["stat_selected"])

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return self.get_context(
            context=context, additional_context=self.additional_context
        )


class TextDetailInfo(DataMixin, DetailView):
    model = Text
    context_object_name = "text"
    slug_url_kwarg = "text_slug"
    template_name = "typing_trainer/text.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_for_pole_count_typed = TextStatistics.objects.values("text").annotate(
            sm=Sum("count_typed")
        )
        additional_context = {
            "title": "Информация о тексте",
            "menu_selected": "text",
            "text_detail_info": True,
            "count_typed_by": queryset_to_dict(
                queryset_for_pole_count_typed,
                group_name="text",
                value_name="sm",
            ),
            "text_slug": self.kwargs["text_slug"],
        }
        return self.get_context(context=context, additional_context=additional_context)


class TextList(DataMixin, ListView):
    model = Text
    context_object_name = "text_list"
    template_name = "typing_trainer/text.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_for_pole_count_typed = TextStatistics.objects.values("text").annotate(
            sm=Sum("count_typed")
        )
        additional_context = {
            "title": "Список текстов",
            "menu_selected": "text",
            "text_detail_info": False,
            "count_typed_by": queryset_to_dict(
                queryset_for_pole_count_typed,
                group_name="text",
                value_name="sm",
            ),
        }
        return self.get_context(context=context, additional_context=additional_context)
    
    def get_queryset(self):
        return Text.objects.all().select_related('author', 'category', 'language')


class AuthorDetailInfo(DataMixin, ListView):
    context_object_name = "author_list"
    slug_url_kwarg = "author_slug"
    template_name = "typing_trainer/author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Информация о авторе",
            "menu_selected": "author",
            "author_name": Author.objects.values("name").get(
                slug=self.kwargs["author_slug"]
            )["name"],
            "author_detail_info": True,
            "author_slug": self.kwargs["author_slug"],
        }
        return self.get_context(context=context, additional_context=additional_context)

    def get_queryset(self):
        return Text.objects.filter(author__slug=self.kwargs["author_slug"]).select_related("category", "language")


class AuthorList(DataMixin, ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "typing_trainer/author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_for_pole_count_typed = AuthorStatistics.objects.values(
            "author"
        ).annotate(sm=Sum("count_typed"))
        queryset_for_pole_text_count = Text.objects.values("author").annotate(
            cnt=Count("text")
        )
        additional_context = {
            "title": "Список авторов",
            "menu_selected": "author",
            "author_detail_info": False,
            "count_typed_by": queryset_to_dict(
                queryset_for_pole_count_typed,
                group_name="author",
                value_name="sm",
            ),
            "text_count_by_author": queryset_to_dict(
                queryset_for_pole_text_count,
                group_name="author",
                value_name="cnt",
            ),
        }
        return self.get_context(context=context, additional_context=additional_context)


class CategoryDetailInfo(DataMixin, ListView):
    context_object_name = "category_list"
    slug_url_kwarg = "category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Информация о категории",
            "menu_selected": "category",
            "category_name": TextCategory.objects.values("title").get(
                slug=self.kwargs["category_slug"]
            )["title"],
            "category_detail_info": True,
            "category_slug": self.kwargs["category_slug"],
        }
        return self.get_context(context=context, additional_context=additional_context)

    def get_queryset(self):
        return Text.objects.filter(category__slug=self.kwargs["category_slug"]).select_related("author", "language")


class CategoryList(DataMixin, ListView):
    model = TextCategory
    context_object_name = "category_list"
    template_name = "typing_trainer/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_for_pole_count_typed = CategoryStatistics.objects.values(
            "category"
        ).annotate(sm=Sum("count_typed"))
        queryset_for_pole_text_count = Text.objects.values("category").annotate(
            cnt=Count("text")
        )
        additional_context = {
            "title": "Список категорий",
            "menu_selected": "category",
            "category_detail_info": False,
            "count_typed_by": queryset_to_dict(
                queryset_for_pole_count_typed,
                group_name="category",
                value_name="sm",
            ),
            "text_count_by_category": queryset_to_dict(
                queryset_for_pole_text_count,
                group_name="category",
                value_name="cnt",
            ),
        }
        return self.get_context(context=context, additional_context=additional_context)


class AddNewText(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTextForm
    template_name = "typing_trainer/post_forms.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Добавление текста",
            "button_text": "Добавить",
            "menu_selected": "text",
        }
        return self.get_context(context=context, additional_context=additional_context)


class AddNewAuthor(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddAuthorForm
    template_name = "typing_trainer/post_forms.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Добавление автора",
            "button_text": "Добавить",
            "menu_selected": "author",
        }
        return self.get_context(context=context, additional_context=additional_context)


class AddNewCategory(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCategoryForm
    template_name = "typing_trainer/post_forms.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = {
            "title": "Добавление категории",
            "button_text": "Добавить",
            "menu_selected": "category",
        }
        return self.get_context(context=context, additional_context=additional_context)


def update_current_property(request, **kwargs):
    if len(kwargs) > 1:
        raise Http404()

    slug, property, model = get_slug_prop_model(kwargs)

    if request.user.is_authenticated:
        user_settings = get_object_or_404(Settings, pk=request.user.pk)
        setattr(user_settings, property, get_object_or_404(model, slug=slug))
        user_settings.save()
        return redirect("index", permanent=True)
    return redirect("login", permanent=True)
