from django.urls import include, path
from . import views

urlpatterns = [
    path('hello', views.hello_view),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
]