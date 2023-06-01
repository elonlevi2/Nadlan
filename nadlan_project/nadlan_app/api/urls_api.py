from django.urls import path
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup", api_views.signup),
    path("login", obtain_auth_token),
    path("check-token", api_views.private),
    path("property/<str:action>", api_views.PropertyApi.as_view()),
    path("contact/<str:action>", api_views.ContactApi.as_view()),
    path("tips/<str:action>", api_views.TipApi.as_view()),
    path("photo", api_views.PhotoApi.as_view(), name='photo'),
    path("properties_sale/<str:action>/<str:rooms>/<str:city>", api_views.PropertyApiPagination.as_view(), name='properties_sale'),
    path("my-properties", api_views.PropertyOfUserApiPagination.as_view(), name='my-properties'),
    path("my-tips", api_views.TipsOfUser.as_view(), name='my-tips'),
    path("user/<str:action>", api_views.UserApi.as_view(), name='user'),
    path("contact/<str:action>", api_views.ContactApi.as_view(), name='contact'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

