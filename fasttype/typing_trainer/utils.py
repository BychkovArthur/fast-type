from datetime import datetime
from .models import Text, TextCategory, Author, Statistics, TextStatistics, AuthorStatistics, CategoryStatistics
from django.http import Http404


def calc_average(average_before, count_before, current_value):
    return round(
        (average_before * count_before + current_value) / (count_before + 1), 2
    )


def update_stat_if_exists(object, data):
    wpm = int(data["wpm"])
    acc = float(data["acc"])
    object.average_wpm = calc_average(object.average_wpm, object.count_typed, wpm)
    object.average_accuracy = calc_average(
        object.average_accuracy, object.count_typed, acc
    )
    object.count_typed += 1

    if wpm > object.best_wpm:
        object.best_wpm = wpm
        object.best_wpm_date = datetime.fromtimestamp(data["date"] // 1000, tz=None)

    object.save()


def update_statistic_by(type, model, data, user):
    kwargs = {"user_statistic": user, type: data[type]}

    if model.objects.filter(**kwargs).exists():
        stat = model.objects.get(**kwargs)
        update_stat_if_exists(stat, data)
    else:
        wpm = int(data["wpm"])
        acc = float(data["acc"])
        model.objects.create(
            **kwargs,
            average_wpm=wpm,
            best_wpm=wpm,
            count_typed=1,
            average_accuracy=acc,
        )


def queryset_to_dict(queryset, group_name, value_name):
    dct = {}
    for dictionary in queryset:
        dct[dictionary[group_name]] = dictionary[value_name]
    return dct


def get_slug_prop_model(kwargs):
    """Возвращает slug, property и model
    для представления, обновляющего текущий
    текст, категорию и автора"""
    if "text_slug" in kwargs:
        slug = kwargs["text_slug"]
        property = "current_text"
        model = Text
    elif "author_slug" in kwargs:
        slug = kwargs["author_slug"]
        property = "current_author"
        model = Author
    elif "category_slug" in kwargs:
        slug = kwargs["category_slug"]
        property = "current_category"
        model = TextCategory
    else:
        raise Http404()
    return slug, property, model


def get_model_by_statistic_type(request_kwargs, additional_context):
    model = None
    if request_kwargs["statistic_type"] == "general":
        model = Statistics
        additional_context["stat_selected"] = "general"

    elif request_kwargs["statistic_type"] == "by_texts":
        model = TextStatistics
        additional_context["stat_selected"] = "text"

    elif request_kwargs["statistic_type"] == "by_categories":
        model = CategoryStatistics
        additional_context["stat_selected"] = "category"

    elif request_kwargs["statistic_type"] == "by_authors":
        model = AuthorStatistics
        additional_context["stat_selected"] = "author"
    else:
        raise Http404()
    return model


class DataMixin:
    def get_context(self, *args, **kwargs):
        context = kwargs["context"]
        additional_context = kwargs["additional_context"]

        for key, value in additional_context.items():
            context[key] = value
        return context
