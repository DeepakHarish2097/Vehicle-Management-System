from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employee, Vehicle, Route, Productivity
from .forms import VehicleForm, RouteForm


# Vehicle Views
@login_required(login_url='login')
def home(request):
    vehicles = Vehicle.objects.all()
    context = {
        "vehicles": vehicles,
        "menu": "menu-vehicle"
    }
    return render(request, 'vms_app/vehicles_list.html', context)


@login_required(login_url='login')
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


# Route Views
@login_required(login_url='login')
def route_list(request):
    routes = Route.objects.all()
    context = {
        "routes": routes,
        "menu": "menu-route"
    }
    return render(request, 'vms_app/routes_list.html', context)


@login_required(login_url='login')
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
        "form_title": "Edit route",
        "menu": "menu-route",
    }
    return render(request, 'vms_app/forms.html', context)
