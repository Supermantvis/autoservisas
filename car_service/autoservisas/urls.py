from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars_list/', views.car_list, name='car_list'),
    path('car_detail/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order_details/<int:pk>/', views.OrderDetailView.as_view(), name='order_details'),
    path('orders/my/', views.UserOrderListView.as_view(), name='user_orders'),
    path('car_list/my/', views.UserCarListView.as_view(), name='user_car_list'),
    path('car_list/car_create/', views.CarCreateView.as_view(), name='car_create'),
    path('order_list/order_create/', views.OrderCreateView.as_view(), name='order_create'),
]
