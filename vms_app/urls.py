from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .serializers import *


urlpatterns = [
    # Permission Denial Urls
    path('no-access/', views.no_access_page, name="no_access_page"),
    path('un-authorised/', views.not_authorised, name="not_authorised"),

    # Auth Urls
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-change-done/', views.password_change_done, name='password_change_done'),


    # /////////////////// App View Urls \\\\\\\\\\\\\\\\\\\

    # Vehicle Urls
    path('', views.home, name='home'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('edit-vehicle/<int:id>/', views.edit_vehicle, name='edit_vehicle'),
    path('deactivate-vehicle/<int:id>/', views.deactivate_vehicle, name='deactivate_vehicle'),
    path('activate-vehicle/<int:id>/', views.activate_vehicle, name='activate_vehicle'),

    # Zone Urls
    path('zone-list/', views.zone_list, name='zone_list'),
    path('add-zone/', views.create_zone, name='create_zone'),
    path('edit-zone/<int:id>/', views.edit_zone, name='edit_zone'),

    # Ward Urls
    path('ward-list/', views.ward_list, name='ward_list'),
    path('add-ward/', views.create_ward, name='create_ward'),
    path('edit-ward/<int:id>/', views.edit_ward, name='edit_ward'),

    # Route Urls
    path('route-list/', views.route_list, name='route_list'),
    path('add-route/', views.add_route, name='add_route'),
    path('edit-route/<int:id>/', views.edit_route, name='edit_route'),
    path('deactivate-route/<int:id>/', views.deactivate_route, name='deactivate_route'),
    path('activate-route/<int:id>/', views.activate_route, name='activate_route'),

    # Staff Urls
    path('staff-list/', views.staff_list, name='staff_list'),
    path('add-staff/', views.create_staff, name='create_staff'),
    path('deactivate-staff/<str:id>/', views.deactivate_staff, name='deactivate_staff'),
    path('activate-staff/<str:id>/', views.activate_staff, name='activate_staff'),
    path('edit-user/', views.edit_user, name='edit_user'),

    # Productivity Urls
    path('productivity-list/', views.productivity_list, name='productivity_list'),
    path('add-productivity/', views.add_productivity, name='add_productivity'),
    path('edit-productivity/<int:id>/', views.edit_productivity, name='edit_productivity'),
    path('end-productivity/<int:id>/', views.end_productivity, name='end_productivity'),
    path('productivity-week-report/', views.productivity_week_report, name='productivity_week_report'),
    path('productivity-month-report/', views.productivity_month_report, name='productivity_month_report'),
    path('productivity-custom-report/', views.productivity_custom_report, name='productivity_custom_report'),

    # testing serializers urls
    path('test/employee/', Employee_lcv.as_view(), name='Employee_lcv'),
    path('test/employee/<int:pk>/', Employee_rud.as_view(), name='Employee_rud'),
    path('test/workshop/', Workshop_lcv.as_view(), name='Workshop_lcv'),
    path('test/workshop/<int:pk>/', Workshop_rud.as_view(), name='Workshop_rud'),
    path('test/zone/', Zone_lcv.as_view(), name='Zone_lcv'),
    path('test/zone/<int:pk>/', Zone_rud.as_view(), name='Zone_rud'),
    path('test/ward/', Ward_lcv.as_view(), name='Ward_lcv'),
    path('test/ward/<int:pk>/', Ward_rud.as_view(), name='Ward_rud'),
    path('test/route/', Route_lcv.as_view(), name='Route_lcv'),
    path('test/route/<int:pk>/', Route_rud.as_view(), name='Route_rud'),
    path('test/vehicle/', Vehicle_lcv.as_view(), name='Vehicle_lcv'),
    path('test/vehicle/<int:pk>/', Vehicle_rud.as_view(), name='Vehicle_rud'),
    path('test/productivity/', Productivity_lcv.as_view(), name='Productivity_lcv'),
    path('test/productivity/<int:pk>/', Productivity_rud.as_view(), name='Productivity_rud'),
    path('test/transfer-register/', Transfer_Register_lcv.as_view(), name='Transfer_Register_lcv'),
    path('test/transfer-register/<int:pk>/', Transfer_Register_rud.as_view(), name='Transfer_Register_rud'),
]

