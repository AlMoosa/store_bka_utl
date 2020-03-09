from django.urls import path, include
from rest_framework import routers

from .views import ItemViewSet, ColorofItemViewSet, SizeOfItemViewSet, SortCategoriesViewSet, \
    ListProductToBasketViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)
router.register(r'color', ColorofItemViewSet)
router.register(r'size', SizeOfItemViewSet)
router.register(r'category', SortCategoriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('order/', OrderViewSet.as_view(), name='booking'),
    path('basket/', ListProductToBasketViewSet.as_view(), name='basket'),
]
