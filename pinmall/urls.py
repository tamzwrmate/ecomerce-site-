from django.urls import include, path
from .views import *


app_name = "pinmall"

urlpatterns = [
    path('', CardListView.as_view(), name='card'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('item-detail/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('add-to-cart/<slug:slug>/', DeatailView.as_view(), name='detail'),
    path('my-cart/', AddToCartView.as_view(), name='cart'),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name='manage-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('interswitch/', Interswitch.as_view(), name='interswitch'),
    path('verify-payment/', VerifyPayment.as_view(), name='verify-payment'),
]