from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^add/$', views.add, name='shopping-cart-add'),
    url(r'^remove/$', views.remove, name='shopping-cart-remove'),
    url(r'^show/$', views.show, name='shopping-cart-show'),
    url(r'^clear/$', views.clear, name='shopping-cart-clear'),
]
