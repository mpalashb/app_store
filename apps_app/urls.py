from django.urls import path
from .views import (
    AppsListView, AppDetailView,
    SearchListView, FilterView)

app_name = 'apps_app'


urlpatterns = [
    path('apps/filter/<str:cat>', FilterView.as_view(), name='apps-filter'),
    path('apps/search', SearchListView.as_view(), name='apps-search'),
    path('apps/<str:app_slug>', AppDetailView.as_view(), name='apps-detail'),
    path('', AppsListView.as_view(), name='apps-list'),
]
