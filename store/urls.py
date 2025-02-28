from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.process_order, name="process_order"),
    path('product/<int:pk>/', views.product_detail, name="product"),
    path('orders/', views.order_history, name="orders"),
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"), 
         name="password_reset_complete"),
    path('product/<int:product_id>/', views.product_view, name='product_view'),
    path('search/', views.search_products, name='search_products'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
]