from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('products/', views.products, name='products'),
    path('addproduct/', views.add_product, name='addproduct'),
    path('update/<int:id>/', views.update_product, name='update'),
    path('delete/<int:id>/', views.delete_product, name='delete'),
    path('user/',views.user_dashboard,name='user'),
    path('logout/',views.logout_user,name='logout/'),

   
]

