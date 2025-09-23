"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_page_view, pw_protect_view, export_information_excel
# from auth.views import login_view, logout_view, register_view
from checkouts.views import checkout_redirect_view, product_price_redirect_view, checkout_finalize_view
from subscriptions.views import subscription_price_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page_view, name="home"),
    path('checkout/sub-price/<int:price_id>/', product_price_redirect_view, name="sub-price-checkout"),
    path('checkout/start/', checkout_redirect_view, name="stripe-checkout-start"),
    path('checkout/success/', checkout_finalize_view, name="stripe-checkout-success"),
    # path('login/', login_view),
    # path('logout/', logout_view),
    # path('register/', register_view),
    path('accounts/', include('allauth.urls')),
    path('export/', export_information_excel, name='export_information_excel'),
    path('protect/', pw_protect_view),
    path('profiles/', include('profiles.urls')),
    path('pricing/', subscription_price_view, name="pricing"),
    path('pricing/<str:interval>', subscription_price_view, name="pricing_interval"),

]
