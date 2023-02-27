from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from myapp.views import index, Login, Register, ProductCreate, ProductUpdate, PurchaseView, purchases_list

urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('create_product/', ProductCreate.as_view(), name='create_product'),
    path('update_product/<int:pk>', ProductUpdate.as_view(), name='update_p'),
    path('purchase/<int:pk>', PurchaseView.as_view(), name='purchase'),
    path('purchases_list/', purchases_list, name='purchases_list'),

]