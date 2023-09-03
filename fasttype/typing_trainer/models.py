from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from django.core.files import File
from django.templatetags.static import static
from django.contrib.staticfiles import finders

from pathlib import Path


class Settings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Пользователь",
    )
    current_theme = models.ForeignKey(
        "Theme",
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Тема",
    )
    show_wpm = models.BooleanField(
        default=True,
        verbose_name="Отображать WPM",
    )
    show_percent_done = models.BooleanField(
        default=True,
        verbose_name="Отображать проценты",
    )
    show_time = models.BooleanField(
        default=True,
        verbose_name="Отображать время",
    )
    show_symbols_count = models.BooleanField(
        default=True,
        verbose_name="Отображать количество символов",
    )
    current_text = models.ForeignKey(
        "Text",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Выбранный текст",
    )
    current_author = models.ForeignKey(
        "Author",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Выбранный автор",
    )
    current_category = models.ForeignKey(
        "TextCategory",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Выбранная категория",
    )

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self):
        return reverse("settings", kwargs={"pk": self.user.pk})

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class Theme(models.Model):
    css = models.TextField(
        unique=True,
        verbose_name="CSS код",
    )

    def __str__(self) -> str:
        return f"Тема №{self.pk}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        import json

        css_colors = json.loads(self.css).items()
        template_url = Path(
            "typing_trainer/static/typing_trainer/css_templates/template.txt"
        )
        new_css_theme = Path(
            f"typing_trainer/static/typing_trainer/css/theme{self.pk}.css"
        )

        with template_url.open("r") as template:
            with new_css_theme.open("w") as css_file:
                for line in template:
                    formated_line = line

                    for key, value in css_colors:
                        formated_line = formated_line.replace(key, value)

                    css_file.write(formated_line)

    class Meta:
        verbose_name = "Темы"
        verbose_name_plural = "Темы"


class Text(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Заголовок",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL",
        # db_index=True, Не указываем индекс, т.к. unique=True подразумевает создание индекса.
    )
    text = models.TextField(
        unique=True,
        verbose_name="Текст",
    )
    length = models.IntegerField(
        verbose_name="Длина",
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Язык",
    )
    category = models.ForeignKey(
        "TextCategory",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Категория",
    )
    author = models.ForeignKey(
        "Author",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Автор",
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Время обновления",
    )
    displayed = models.BooleanField(
        default=True,
        verbose_name="Отображается",
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("text_info", kwargs={"text_slug": self.slug})

    def save(self, *args, **kwargs):
        self.text = self.text.replace("—", "-")
        self.text = self.text.replace("«", '"')
        self.text = self.text.replace("»", '"')
        if not self.slug:
            self.slug = slugify(self.title)
        self.length = len(self.text.replace("\r", ""))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"


class Language(models.Model):
    code = models.SlugField(
        max_length=7,
        unique=True,
        verbose_name="Код",
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Язык",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"


class TextCategory(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL",
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("category_info", kwargs={"category_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Имя",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL",
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("author_info", kwargs={"author_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Statistics(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Пользователь",
    )
    rating = models.FloatField(
        default=0,
        verbose_name="Рейтинг",
    )
    last_text = models.ForeignKey(
        Text,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        related_name="last_typed_text",
        verbose_name="Последний текст",
    )
    average_wpm = models.FloatField(
        default=0,
        verbose_name="Средний WPM",
    )
    best_wpm = models.FloatField(
        default=0,
        verbose_name="Лучший WPM",
    )
    best_wpm_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата лучшего WPM",
    )
    count_typed = models.IntegerField(
        default=0,
        verbose_name="Текстов напечатано",
    )
    average_accuracy = models.FloatField(
        default=100,
        verbose_name="Средний процент ошибок",
    )
    text_statistic = models.ManyToManyField(
        Text,
        through="TextStatistics",
    )
    category_statistic = models.ManyToManyField(
        TextCategory,
        through="CategoryStatistics",
    )
    author_statistic = models.ManyToManyField(
        Author,
        through="AuthorStatistics",
    )

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self):
        return reverse(
            "user_statistics", kwargs={"pk": self.user.pk, "statistic_type": "general"}
        )

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
        ordering = (
            "-rating",
            "-average_wpm",
            "-average_accuracy",
            "-best_wpm",
            "-count_typed",
            "best_wpm_date",
        )


class BaseStatistics(models.Model):
    user_statistic = models.ForeignKey(
        Statistics,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    average_wpm = models.FloatField(
        default=0,
        verbose_name="Средний WPM",
    )

    best_wpm = models.FloatField(
        default=0,
        verbose_name="Лучший WPM",
    )

    best_wpm_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата лучшего WPM",
    )

    count_typed = models.IntegerField(
        default=0,
        verbose_name="Текстов напечатано",
    )

    average_accuracy = models.FloatField(
        default=100,
        verbose_name="Средний процент ошибок",
    )

    def __str__(self) -> str:
        return str(self.user_statistic)

    class Meta:
        abstract = True


class TextStatistics(BaseStatistics):
    text = models.ForeignKey(
        Text,
        on_delete=models.CASCADE,
        verbose_name="Текст",
    )

    class Meta:
        verbose_name = "Статистика по текстам"
        verbose_name_plural = "Статистика по текстам"
        ordering = (
            "text",
            "-average_wpm",
            "-average_accuracy",
            "-best_wpm",
            "-count_typed",
            "best_wpm_date",
        )


class CategoryStatistics(BaseStatistics):
    category = models.ForeignKey(
        TextCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Статистика по категориям"
        verbose_name_plural = "Статистика по категориям"
        ordering = (
            "category",
            "-average_wpm",
            "-average_accuracy",
            "-best_wpm",
            "-count_typed",
            "best_wpm_date",
        )


class AuthorStatistics(BaseStatistics):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Статистика по авторам"
        verbose_name_plural = "Статистика по авторам"
        ordering = (
            "author",
            "-average_wpm",
            "-average_accuracy",
            "-best_wpm",
            "-count_typed",
            "best_wpm_date",
        )
