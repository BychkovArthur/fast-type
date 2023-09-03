from django.contrib import admin
from .models import *


class SettingsAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "current_text",
        "current_author",
        "current_category",
        "show_percent_done",
        "show_wpm",
        "show_symbols_count",
        "show_time",
        "current_theme",

    )
    list_display = (
        "user",
        "current_text",
        "current_author",
        "current_category",
        "show_percent_done",
        "show_wpm",
        "show_symbols_count",
        "show_time",
        "current_theme",
    )
    list_editable = (
        "show_percent_done",
        "show_wpm",
        "show_symbols_count",
        "show_time",
    )
    empty_value_display = "null"
    search_fields = ("user__username",)


class TextAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "slug",
        "text",
        "displayed",
        "category",
        "author",
        "language",
        "time_create",
        "time_update",
    )
    list_display = (
        "id",
        "title",
        "slug",
        "displayed",
        "category",
        "author",
        "language",
        "length",
    )
    list_display_links = (
        "id",
        "title",
        "slug",
    )
    list_editable = ("displayed",)
    search_fields = (
        "title",
        "text"
    )
    readonly_fields = (
        "time_create",
        "time_update"
    )
    empty_value_display = "null"
    prepopulated_fields = {"slug": ("title",)}


class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "code"
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug"
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug"
    )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rating",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
        "last_text",
    )
    fields = (
        "user",
        "rating",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
        "last_text",
    )
    readonly_fields = ("best_wpm_date",)
    search_fields = ('user__username', )

class TextStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "user_statistic",
        "text",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
    )
    fields = (
        "user_statistic",
        "text",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
    )
    readonly_fields = ("best_wpm_date",)
    search_fields = (
        "text__title",
        "user_statistic__user__username"
    )


class TextCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "user_statistic",
        "category",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
    )
    fields = (
        "user_statistic",
        "category",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
    )
    readonly_fields = ("best_wpm_date",)
    search_fields = (
        "category__title",
        "user_statistic__user__username"
    )


class TextAuthorAdmin(admin.ModelAdmin):
    list_display = (
        "user_statistic",
        "author",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
    )
    fields = (
        "user_statistic",
        "author",
        "average_wpm",
        "best_wpm",
        "best_wpm_date",
        "count_typed",
        "average_accuracy",
    )
    readonly_fields = ("best_wpm_date",)
    search_fields = (
        "author__name",
        "user_statistic__user__username"
    )


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Theme)
admin.site.register(Text, TextAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(TextCategory, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(TextStatistics, TextStatisticsAdmin)
admin.site.register(CategoryStatistics, TextCategoryAdmin)
admin.site.register(AuthorStatistics, TextAuthorAdmin)
