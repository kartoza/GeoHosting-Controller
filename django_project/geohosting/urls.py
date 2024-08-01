# coding=utf-8
"""GeoHosting."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from geohosting.api.activity import (
    ActivityViewSet, ActivityTypeViewSet
)
from geohosting.api.checkout import CheckoutStripeSessionAPI
from geohosting.api.product import ProductViewSet
from geohosting.api.token import CreateToken
from geohosting.api.webhook import WebhookView
from geohosting.views.auth import (
    CustomAuthToken, logout, ValidateTokenView, RegisterView
)
from geohosting.views.home import HomeView
from geohosting.views.products import fetch_products

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'products', ProductViewSet)
router.register(
    r'activity_types', ActivityTypeViewSet, basename='activity_types'
)

api = [
    path('webhook/', WebhookView.as_view(), name='webhook-api'),
    path('fetch-products/',
         fetch_products,
         name='fetch_products'),
    path('token/create',
         CreateToken.as_view(), name='create-token'),
    path('auth/login/',
         CustomAuthToken.as_view(), name='api_login'),
    path('auth/register/',
         RegisterView.as_view(), name='register'),
    path('auth/logout/', logout, name='api_logout'),
    path('auth/validate-token/',
         ValidateTokenView.as_view(), name='validate-token'),
    path(
        'package/<pk>/checkout',
        CheckoutStripeSessionAPI.as_view(),
        name='checkout_session'
    ),
]
api += router.urls

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/', include(api)),
]
