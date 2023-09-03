from django import template
from typing_trainer.models import TextStatistics, CategoryStatistics, AuthorStatistics
from typing_trainer.models import Settings

register = template.Library()

@register.filter(name='ord')
def ord_tag(value):
    return ord(value)

@register.filter(name='replace')
def replace_tag(value, args):
    args = args.split(',')
    old = args[0]
    new = args[1]
    return value.replace(old, new)

@register.filter(name='getattr')
def get_obj_attr(value, attr_name):
    return getattr(value, attr_name)

@register.filter(name='get_absolute_url_for')
def get_absolute_url_for(value, attr_name):
    return getattr(value, attr_name).get_absolute_url()


@register.filter(name='get_dict_value_by_key')
def get_dict_value_by_key(dictionary, key):
    return dictionary.get(key, None)

def get_type(object):
    if isinstance(object, TextStatistics):
        return 'text'
    if isinstance(object, CategoryStatistics):
        return 'category'
    if isinstance(object, AuthorStatistics):
        return 'author'

@register.filter(name='get_path_to_css')
def get_path_to_css(user):
    theme_num = '1'
    if user.is_authenticated:
        theme_num = Settings.objects.values('current_theme__pk').get(pk=user.pk)['current_theme__pk']
    return f'typing_trainer/css/theme{theme_num}.css'


@register.filter(name='group_by')
def group_by(value):
    '''Функция для группировки статистика по
    1) Определенному тексту
    2) Определенной категории
    3) Определенному автору'''
    
    if len(value) == 0:
        return
    
    grouped_by_type = []
    current_group = []
    previous = None
    grouping_type = get_type(value[0])
    
    for field in value:
        
        if previous is None:
            previous = getattr(field, grouping_type)
            current_group += [field]
        else:
            if previous == getattr(field, grouping_type):
                current_group += [field]
            else:
                grouped_by_type += [current_group]
                current_group = [field]
                previous = getattr(field, grouping_type)
    grouped_by_type += [current_group]
    return grouped_by_type