from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('auth_login/', views.auth_login, name="auth_login"),
    path('signout', views.signout, name="signout"),
    path('exp_tracker/', views.exp_tracker, name='exp_tracker'),
    path('exp_tracker_data/', views.exp_tracker_data, name='exp_tracker_data'),
    path('more_stats/', views.more_stats, name='more_stats'),
    path('payment_method_data/', views.payment_method_data, name='payment_method_data'),
    path('category_expenditure/', views.category_expenditure, name='category_expenditure'),
    path('expense_budget/', views.expense_budget, name='expense_budget'),
    path('payment_page/', views.payment_page, name='payment_page'),
    path('savings_tracker/', views.savings_tracker, name='savings_tracker'),
    path('savings_tracker_data/', views.savings_tracker_data, name='savings_tracker_data'),
    path('dynamic_order/', views.dynamic_order, name='dynamic_order'),
    path('ai_payment_method/', views.ai_payment_method, name='ai_payment_method'),
    path('orders_page', views.orders_page, name='orders_page'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)