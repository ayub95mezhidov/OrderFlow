from django.urls import path
from .views import (welcome, CustomerListView, orders, add_customer, customers_with_debt,
                    add_order, update_order, orders_remove, orders_acc_remove, update_order_status,
                    update_payment_status, customer_debt,
                    new_orders_all_customers, completed_orders_all_customers, in_progress_orders_all_customers, not_paid_orders_all_customers, paid_orders_all_customers,
                    customer_update, add_order_accessories,
                    customers_remove, update_payment_status_accessories, add_order_for_orders,
                    scan_drawings, scan_confirm)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('customer/', CustomerListView.as_view(),  name='customers'),
    path('', welcome,  name='welcome'),
    path('add_customer/', add_customer,  name='add_customer'),
    path('<int:customer_id>/update/', customer_update, name='customer_update'),
    path('customer/<int:customer_id>/orders', orders,  name='orders'),
    path('customers_with_debt', customers_with_debt,  name='customers_with_debt'),

    path('orders/add/', add_order_for_orders, name='add_order'),
    path('orders/add/<int:customer_id>/', add_order, name='add_order_for_customer'),
    path('orders/update/<int:order_id>/', update_order, name='update_order'),
    path('orders/add/accessories/<int:customer_id>/', add_order_accessories, name='add_order_accessories'),

    path('customer/remove/<int:customer_id>/', customers_remove, name='customers_remove'),
    path('orders/remove/<int:order_id>/', orders_remove, name='orders_remove'),
    path('orders/accessories/remove/<int:order_id>/', orders_acc_remove, name='orders_acc_remove'),

    path('orders/<int:order_id>/update_status', update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/update_payment_status', update_payment_status, name='update_payment_status'),
    path('orders/<int:accessories_id>/update_payment_status_accessories', update_payment_status_accessories, name='update_payment_status_accessories'),
    path('orders/<int:customer_id>/customer_debt', customer_debt, name='customer_debt'),

    path('new_orders_all/', new_orders_all_customers, name='new_orders_all'),
    path('in_progress_orders_all/', in_progress_orders_all_customers, name='in_progress_orders'),
    path('completed_orders_all/', completed_orders_all_customers, name='completed_orders'),
    path('not_paid_orders_all_customers/', not_paid_orders_all_customers, name='not_paid_orders'),
    path('paid_orders_all_customers/', paid_orders_all_customers, name='paid_orders'),

    path('orders/scan/', scan_drawings, name='scan_drawings'),
    path('orders/scan/<int:customer_id>/', scan_drawings, name='scan_drawings_customer'),
    path('orders/scan/confirm/', scan_confirm, name='scan_confirm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)