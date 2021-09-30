from django.conf.urls import url
from django.urls import path
from . import views


# Definimos una lista con las URLs que soporta nuestra app
# notar que en la urls.py principal del proyecto (DjangoTest) se usa
# include('FirstApp.urls') para incluir estas URLs.
# También notar que en el settings.py de DjantoTest se incluyó en INSTALLED_APPS esta
# app, de lo contrario no funcionaría.
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'create_cat', views.create_cat, name='create_cat'),
    url(
        r'create_animal/(?P<name>[^\s/]+)/(?P<weight>\d+)$',
        views.create_animal, name='create_animal'
    ),
    path(r'review_animals', views.review_animals, name='review_animals'),
    url(r'^class_based_view/$', views.AnimalsListView.as_view(), name='class_based_view'),
]
