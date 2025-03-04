from django.urls import path

from apps.views import ProductListView, sell_product, ProductFormView, FinishProductListView, sell_finish_product, \
    FinishProductFormView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('sell-product/', sell_product, name='sell_product'),
    path('product_create', ProductFormView.as_view(), name='product_create'),
    path('finish_product_list', FinishProductListView.as_view(), name='finish_product_list'),
    path('sell_finish_product/', sell_finish_product, name='sell_finish_product'),
    path('finish_product_create', FinishProductFormView.as_view(), name='finish_product_create'),
]
