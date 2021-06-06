from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import  UserLoginForm

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update-item'),
    path('process_order/', views.process_order, name='process-order'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'login/', 
        LoginView.as_view(
            template_name="store/login.html",
            authentication_form=UserLoginForm,
        ), 
        name='login'
    ),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
]
