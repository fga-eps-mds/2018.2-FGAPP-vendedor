from django.conf.urls import url
from products import views
from django.conf.urls import include
from .views import ProductDelete
from django.urls import path

urlpatterns = [
    url(r'^products/$', views.ProductList.as_view()),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view()),

    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    path('api/product_delete', ProductDelete),
]
