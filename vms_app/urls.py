from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Permission Denial Urls
    path('no-access/', views.no_access_page, name="no_access_page"),
    path('un-authorised/', views.not_authorised, name="not_authorised"),

    # Auth Urls
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    # App View Urls

    # Vehicle Urls
    path('', views.home, name='home'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('edit-vehicle/<int:id>/', views.edit_vehicle, name='edit_vehicle'),
    path('deactivate-vehicle/<int:id>/', views.deactivate_vehicle, name='deactivate_vehicle'),
    path('activate-vehicle/<int:id>/', views.activate_vehicle, name='activate_vehicle'),

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
]

