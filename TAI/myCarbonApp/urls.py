from django.urls import path
from . import views

app_name = 'myCarbonApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('offset-now/', views.offsets, name='offset-now'),
    path('projects/', views.projects, name='projects'),
    path('car-emission-offset/', views.car_emission_offset, name='car-emission-offset'),
    path('house-emission-offset/', views.household_emission_offset, name='house-emission-offset'),
    path('buy-cert-cos/', views.buy_certified_cos, name='buy-cert-cos'),
    path('gift-cert/', views.buy_gift_certificate, name='gift-cert'),
    path('tours-offset/', views.tours_offset, name='tours-offset'),
    path('business-offset/', views. business_offset, name='business-offset'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('delete-from-cart/<int:items>', views.delete_from_cart, name='delete-from-cart'),
    path('pay/', views.pay_page, name='pay'),
    path('logout/', views.logout, name='logout'),
]