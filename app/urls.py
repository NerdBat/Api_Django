from django.urls import path
from . import views

urlpatterns = [
    path("test_json_view", views.test_json_view, name="test_json_view"),
    path("greeting_post", views.greeting_post, name="greeting_post"),
    path("products/list", views.get_all_products, name="get_all_products"),
    path("products/most_expensive/", views.get_most_expensive_product, name="most_expensive_product"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/update/<int:product_id>/", views.update_product, name="update_product"),
    path("products/page/", views.paginated_products, name="paginated_products")
]