from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employee, Vehicle, Route, Productivity
from .forms import VehicleForm, RouteForm, EmployeeRegistrationForm, ProductivityForm
from .decorators import superuser_required, active_required
from django.contrib.auth import logout
from django.utils import timezone


@login_required(login_url='login')
@active_required
def no_access_page(request):
    return render(request, 'registration/no_access.html')


def not_authorised(request):
    return render(request, 'registration/inactive.html')


# ------------------- Vehicle Views -------------------
@login_required(login_url='login')
@active_required
def home(request):
    vehicles = Vehicle.objects.all()
    context = {
        "vehicles": vehicles,
        "menu": "menu-vehicle"
    }
    return render(request, 'vms_app/vehicles_list.html', context)


@login_required(login_url='login')
@active_required
def add_vehicle(request):
    form = VehicleForm()
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            current_user = request.user
            vehicle.created_by = current_user
            vehicle.updated_by = current_user
            vehicle.save()
            return redirect('home')
    context = {
        "form": form,
        "form_title": "Add Vehicle",
        "menu": "menu-vehicle",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_vehicle(request, id: int):
    vehicle = Vehicle.objects.get(pk=id)
    form = VehicleForm(instance=vehicle)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            current_user = request.user
            vehicle.updated_by = current_user
            vehicle.save()
            return redirect('home')
    context = {
        "form": form,
        "form_title": "Edit Vehicle",
        "menu": "menu-vehicle",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
@superuser_required
def deactivate_vehicle(request, id: int):
    vehicle = Vehicle.objects.get(pk=id)
    if vehicle:
        vehicle.is_active = False
        vehicle.save()
        return redirect('home')


@login_required(login_url='login')
@active_required
@superuser_required
def activate_vehicle(request, id: int):
    vehicle = Vehicle.objects.get(pk=id)
    if vehicle:
        vehicle.is_active = True
        vehicle.save()
        return redirect('home')


# ------------------- Route Views -------------------
@login_required(login_url='login')
@active_required
def route_list(request):
    routes = Route.objects.all()
    context = {
        "routes": routes,
        "menu": "menu-route"
    }
    return render(request, 'vms_app/routes_list.html', context)


@login_required(login_url='login')
@active_required
def add_route(request):
    form = RouteForm()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            current_user = request.user
            route.created_by = current_user
            route.updated_by = current_user
            route.save()
            return redirect('route_list')
    context = {
        "form": form,
        "form_title": "Add Route",
        "menu": "menu-route",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_route(request, id: int):
    route = Route.objects.get(pk=id)
    form = RouteForm(instance=route)
    if request.method == "POST":
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            route = form.save(commit=False)
            current_user = request.user
            route.updated_by = current_user
            route.save()
            return redirect('route_list')
    context = {
        "form": form,
        "form_title": "Edit Route",
        "menu": "menu-route",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
@superuser_required
def deactivate_route(request, id: int):
    route = Route.objects.get(pk=id)
    if route:
        route.is_active = False
        route.save()
        return redirect('route_list')


@login_required(login_url='login')
@active_required
@superuser_required
def activate_route(request, id: int):
    route = Route.objects.get(pk=id)
    if route:
        route.is_active = True
        route.save()
        return redirect('route_list')


# ------------------- Staff Views -------------------
@login_required(login_url='login')
@active_required
@superuser_required
def staff_list(request):
    # check_superuser(request)
    employees = Employee.objects.all()
    context = {
        "employees": employees,
        "menu": "menu-staff"
    }
    return render(request, 'vms_app/staff_list.html', context)


@login_required(login_url='login')
@active_required
@superuser_required
def create_staff(request):
    # check_superuser(request)
    form = EmployeeRegistrationForm()
    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    context = {
        'form': form,
        "form_title": "Add Staff",
        "menu": "menu-staff",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
@superuser_required
def deactivate_staff(request, id:str):
    employee = Employee.objects.get(pk=id)
    if employee:
        employee.is_active = False
        employee.save()
        return redirect('staff_list')


@login_required(login_url='login')
@active_required
@superuser_required
def activate_staff(request, id:str):
    employee = Employee.objects.get(pk=id)
    if employee:
        employee.is_active = True
        employee.save()
        return redirect('staff_list')


# ------------------- Productivity Views -------------------
@login_required(login_url='login')
@active_required
def productivity_list(request):
    productivity = Productivity.objects.all()
    context = {
        "menu": "menu-productivity",
        "productivity_list": productivity
    }
    return render(request, 'vms_app/productivity_list.html', context)


@login_required(login_url='login')
@active_required
def add_productivity(request):
    form = ProductivityForm()

    if request.method == "POST":
        form = ProductivityForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            productivity = form.save(commit=False)
            total_estimation = 0
            for route in clean_data['routes']:
                total_estimation += route.estimation
            productivity.estimation = total_estimation
            productivity.save()
            productivity.routes.set(clean_data['routes'])
            return redirect('productivity_list')

    context = {
        "form": form,
        "menu": "menu-productivity",
        "form_title": "Add Productivity",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_productivity(request, id: int):
    productivity = Productivity.objects.get(pk=id)
    form = ProductivityForm(instance=productivity)

    if request.method == "POST":
        form = ProductivityForm(request.POST, instance=productivity)
        if form.is_valid():
            clean_data = form.cleaned_data
            productivity = form.save(commit=False)
            total_estimation = 0
            for route in clean_data['routes']:
                total_estimation += route.estimation
            productivity.estimation = total_estimation
            productivity.save()
            productivity.routes.set(clean_data['routes'])
            return redirect('productivity_list')

    context = {
        "form": form,
        "menu": "menu-productivity",
        "form_title": "Edit Productivity",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def end_productivity(request, id: int):
    productivity = Productivity.objects.get(pk=id)
    productivity.end = timezone.now()
    productivity.day_production = round((timezone.now()-productivity.start).total_seconds()/60)
    productivity.save()
    return redirect('productivity_list')
