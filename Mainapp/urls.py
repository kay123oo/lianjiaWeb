from django.urls import path,re_path
from . import views


urlpatterns = [
    path('', views.vison_test),
    path('ditu/<str:community>', views.ajax_update, name='ajax-list'),
    path('<str:city>/', views.group_by_city),
    path('<str:city>/ditu', views.find_by_map),
    re_path('^(?P<city>[a-z]{2})\/(?P<conditions>[a-z0-9]+[0-9]{1})\/', views.get_by_conditions),
    path('<str:city>/<str:district>/', views.group_by_district),
    re_path('^(?P<city>[a-z]{2})\/(?P<district>\w+)\/(?P<conditions>[a-z0-9]+[0-9]{1})\/', views.get_by_conditions),
    path('<str:city>/<str:district>/<str:microdistrict>/', views.group_by_microdistrict),
    re_path('^(?P<city>[a-z]{2})\/(?P<district>\w+)\/(?P<microdistrict>\w+)\/(?P<conditions>[a-z0-9]+[0-9]{1})\/',
            views.get_by_conditions)

    ]
