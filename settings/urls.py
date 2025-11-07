from django.urls import path

from .views import price_settings, price_update, price_create_canvases, price_accessories_create, price_ceiling_remove, price_accessories_remove, price_accessories_update

urlpatterns = [
    path('', price_settings, name='price_settings'),
    path('price_create_can', price_create_canvases, name='price_create_canvases'),
    path('price_accessories_create', price_accessories_create, name='price_accessories_create'),
    path('price/<int:price_id>/update', price_update, name='price_update'),
    path('price_accessories/<int:price_id>/update', price_accessories_update, name='price_accessories_update'),

    path('price_ceiling/remove/<int:price_id>/', price_ceiling_remove, name='price_ceiling_remove'),
    path('price_accessories/remove/<int:price_id>/', price_accessories_remove, name='price_accessories_remove'),
]
