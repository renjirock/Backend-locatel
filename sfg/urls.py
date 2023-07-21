"""
URL configuration for sfg project.

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
from django.urls import path
from rest_framework.authtoken import views
from api.views import Logout, RegisterView
from bankAccount.views import Account, Balance
from deposits.views import Deposits
from withdraw.views import Withdraw, ConfirmWithdraw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/generate_token/', views.obtain_auth_token),
    path('api/v1.0/logout/', Logout.as_view()),
    path('api/v1.0/register/', RegisterView.as_view(), name='auth_register'),
    path('api/v1.0/account', Account.as_view()),
    path('api/v1.0/account/balance', Balance.as_view()),
    path('api/v1.0/deposits', Deposits.as_view()),
    path('api/v1.0/withdraw', Withdraw.as_view()),
    path('api/v1.0/withdraw/confirm', ConfirmWithdraw.as_view()),
]
