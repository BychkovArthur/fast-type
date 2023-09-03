from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_statistic/', add_statistic, name='add_stat'),
    path('settings/<int:pk>/', UserSettings.as_view(), name='settings'),
    path('user_statistics/<int:pk>/<statistic_type>', UserStatistics.as_view(), name='user_statistics'),
    path('leaderboard/<statistic_type>', Leaderboard.as_view(), name='leaderboard'),
    path('text/<slug:text_slug>/', TextDetailInfo.as_view(), name='text_info'),
    path('text_list/', TextList.as_view(), name='textlist'),
    path('author/<slug:author_slug>/', AuthorDetailInfo.as_view(), name='author_info'),
    path('author_list/', AuthorList.as_view(), name='authorlist'),
    path('category/<slug:category_slug>/', CategoryDetailInfo.as_view(), name='category_info'),
    path('category_list/', CategoryList.as_view(), name='categorylist'),
    path('add_text/', AddNewText.as_view(), name='addtext'),
    path('add_author/', AddNewAuthor.as_view(), name='addauthor'),
    path('add_category/', AddNewCategory.as_view(), name='addcategory'),
    path('update_current_text/<slug:text_slug>', update_current_property, name='updatecurrenttext'),
    path('update_current_author/<slug:author_slug>', update_current_property, name='updatecurrentauthor'),
    path('update_current_category/<slug:category_slug>', update_current_property, name='updatecurrentcategory'),
    path('random_choice/<str:type>/', choose_random, name='chooserandom'),
    
]
