from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import superuser_required, active_required
from django.contrib.auth import logout
from django.utils import timezone
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
import datetime


@login_required(login_url='login')
@active_required
def no_access_page(request):
    return render(request, 'registration/no_access.html')


def not_authorised(request):
    return render(request, 'registration/inactive.html')


# /////////////////// Vehicle Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def home(request):
    queries = {
        "active": {"is_active": True},
        "in_active": {"is_active": False},
        "working": {"is_working": True, "is_active": True},
        "not_working": {"is_working": False, "is_active": True},
    }
    vehicles = Vehicle.objects.filter(**queries["active"])
    query = request.GET.get("query", None)
    if query and query in queries:
        vehicles = Vehicle.objects.filter(**queries[query])

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


# /////////////////// Zone Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def zone_list(request):
    zones = Zone.objects.all()
    context = {
        "zones": zones,
        "menu": "menu-zone"
    }
    return render(request, 'vms_app/zone_list.html', context)


@login_required(login_url='login')
@active_required
def create_zone(request):
    form = ZoneForm()
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zone_list')
    context = {
        "form": form,
        "form_title": "Add Zone",
        "menu": "menu-zone",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_zone(request, id: int):
    zone = Zone.objects.get(pk=id)
    form = ZoneForm(instance=zone)
    if request.method == 'POST':
        form = ZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('zone_list')
    context = {
        "form": form,
        "form_title": "Edit Zone",
        "menu": "menu-zone",
    }
    return render(request, 'vms_app/forms.html', context)


# /////////////////// Ward Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def ward_list(request):
    wards = Ward.objects.all()
    context = {
        "wards": wards,
        "menu": "menu-ward"
    }
    return render(request, 'vms_app/ward_list.html', context)


@login_required(login_url='login')
@active_required
def create_ward(request):
    form = WardForm()
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ward_list')
    context = {
        "form": form,
        "form_title": "Add Ward",
        "menu": "menu-ward",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_ward(request, id: int):
    ward = Ward.objects.get(pk=id)
    form = WardForm(instance=ward)
    if request.method == 'POST':
        form = WardForm(request.POST, instance=ward)
        if form.is_valid():
            form.save()
            return redirect('ward_list')
    context = {
        "form": form,
        "form_title": "Edit Ward",
        "menu": "menu-ward",
    }
    return render(request, 'vms_app/forms.html', context)


# /////////////////// Route Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def route_list(request):
    search_active = False if request.GET.get('query', None) == "in_active" else True
    routes = Route.objects.filter(is_active=search_active)
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


# /////////////////// Staff Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
@superuser_required
def staff_list(request):
    search_active = False if request.GET.get('query', None) == "in_active" else True
    employees = Employee.objects.filter(is_active=search_active).order_by("-is_superuser")
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
def deactivate_staff(request, id: str):
    employee = Employee.objects.get(pk=id)
    if employee:
        employee.is_active = False
        employee.save()
        return redirect('staff_list')


@login_required(login_url='login')
@active_required
@superuser_required
def activate_staff(request, id: str):
    employee = Employee.objects.get(pk=id)
    if employee:
        employee.is_active = True
        employee.save()
        return redirect('staff_list')


@login_required(login_url='login')
@active_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')


@login_required(login_url='login')
@active_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change.html', {'form': form})


@login_required(login_url='login')
@active_required
def edit_user(request):
    form = EmployeeEditForm(instance=request.user)
    if request.method == 'POST':
        form = EmployeeEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
        "form_title": "Edit User",
        "menu": "menu-staff",
    }
    return render(request, 'vms_app/edit_profile.html', context)


# /////////////////// Shift Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def shift_list(request):
    shift = Shift.objects.filter(created_on__date=timezone.now().date())
    context = {
        "menu": "menu-shift",
        "shift_list": shift,
        "type": type,
    }
    return render(request, 'vms_app/shift_views/shift_list.html', context)


@login_required(login_url='login')
@active_required
def start_shift(request):
    form = ShiftForm()

    if not request.user.is_superuser:
        vehicle = Vehicle.objects.filter(supervisor=request.user, is_working=False)
        routes = Route.objects.filter(supervisor=request.user, is_working=False, is_active=True)

        form.fields['vehicle'].queryset = vehicle
        form.fields['routes'].queryset = routes
    else:
        form.fields['vehicle'].queryset = Vehicle.objects.filter(is_working=False)
        form.fields['routes'].queryset = Route.objects.filter(is_working=False, is_active=True)

    if request.method == "POST":
        form = ShiftForm(request.POST, request.FILES)
        if form.is_valid():
            clean_data = form.cleaned_data
            shift = form.save()
            vehicle = shift.vehicle
            vehicle.is_working = True
            vehicle.save()
            # TripHistory operations
            trip = TripHistory()
            trip.shift = shift
            trip.vehicle=vehicle
            trip.save()
            
            # trip.is_current will be set True by default. We have off it while rotating the shift
            # so that we can close the trip while ending shift.
            # trip_count will save by overwritten save method in models.py
            # shift.routes.set(clean_data['routes'])
            return redirect('shift_list')

    context = {
        "form": form,
        "menu": "menu-shift",
        "form_title": "Start Shift",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_shift(request, id: int):
    shift = Shift.objects.get(pk=id)
    vehicle = shift.vehicle
    vehicle.is_working = False
    vehicle.save()
    for route in shift.routes.all():
        route.is_working = False
        route.save()
    form = ShiftForm(instance=shift)

    if not request.user.is_superuser:
        vehicle = Vehicle.objects.filter(supervisor=request.user, is_working=False)
        routes = Route.objects.filter(supervisor=request.user, is_working=False, is_active=True)

        form.fields['vehicle'].queryset = vehicle
        form.fields['routes'].queryset = routes

    if request.method == "POST":
        form = ShiftForm(request.POST, request.FILES, instance=shift)
        if form.is_valid():
            clean_data = form.cleaned_data
            shift = form.save(commit=False)
            total_km_estimation = 0
            total_time_estimation = 0
            for route in clean_data['routes']:
                total_time_estimation += route.time_estimation
                total_km_estimation += route.time_estimation
                route.is_working = True
                route.save()
            shift.time_estimation = total_time_estimation
            shift.km_estimation = total_km_estimation
            shift.save()
            vehicle = shift.vehicle
            vehicle.is_working = True
            vehicle.save()
            shift.routes.set(clean_data['routes'])
            return redirect('shift_list')

    context = {
        "form": form,
        "menu": "menu-shift",
        "form_title": "Edit Shift",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def rotate_trip(request, id: int): # We gave to use the trip_object id now
    shift = Shift.objects.get(pk=id)
    trip = shift.shift_trips_set.all().get(is_current=True)
    # trip = TripHistory.objects.get(pk=id)
    form = RotateTripForm()
    if request.method == "POST":
        form = RotateTripForm(request.POST, instance=trip)
        if form.is_valid():
            trip_obj = form.save(commit=False)
            trip_obj.is_current=False
            trip_obj.trip_end_time = timezone.now()
            trip_obj.save()
            # trip_efficiency will be save by overwritten save method in models.py
            
            # Starting next trip
            next_trip = TripHistory()
            next_trip.shift = shift
            next_trip.vehicle=shift.vehicle
            next_trip.save()
            return redirect('shift_list')
    context = {
        "form": form,
        "menu": "menu-shift",
        "form_title": "Rotate Trip",
    }
    return render(request, 'vms_app/forms.html', context)

    return redirect('testing_new')


@login_required(login_url='login')
@active_required
def end_shift(request, id: int): # this id belongs to trip_object here now
    '''Actually it is Trip closing function
    We are closing the last trip and  closing the corresponding shift parallelly.
    Flaw is that the trip will be closed in Dump Yard. Shift will be closed in Vehicle Set. 
    There is km and time difference between 2 points
    This flaw --- we can fix later '''
    
    shift = Shift.objects.get(pk=id)
    trip = shift.shift_trips_set.all().get(is_current=True)
    print(trip)
    # trip = TripHistory.objects.get(pk=id)
    
    # print(trip)
    # shift = trip.shift
    # print(shift)
    
    form = ShiftEndForm()
    if request.method == "POST":
        form = ShiftEndForm(request.POST, request.FILES)
        if form.is_valid():
            clean_data = form.cleaned_data
            print(clean_data)
            shift.shift_remark=clean_data['shift_remark']
            shift.in_km=clean_data['in_km']
            shift.end_image=clean_data['end_image']
            shift.end_time = timezone.now()
            vehicle = shift.vehicle
            vehicle.is_working = False
            vehicle.save()
            shift.save()

            # closing Trip
            trip.trip_load=clean_data['trip_load']
            trip.trip_remark = clean_data['trip_remark']
            trip.trip_end_time=timezone.now()
            trip.is_current=False
            last_trip = trip.save()
            # shift.save()
            
            return redirect('shift_list')
    
    
    context = {
    "form": form,
    "menu": "menu-shift",
    "form_title": "End Shift",
    }
    return render(request, 'vms_app/forms.html', context)
    


# /////////////////// Productivity Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def productivity_list(request):
    # return HttpResponse("Test")
    shifts = Shift.objects.filter(end_time__isnull=False)
    
    context = {
        "menu": "menu-productivity",
        "shifts": shifts,
    }
    return render(request, 'vms_app/productivity_list.html', context)


@login_required(login_url='login')
@active_required
def shift_details(request, id: int):
    shift = Shift.objects.get(pk=id)
    context = {
        "menu": "menu-productivity",
        "shift": shift,
    }
    return render(request, 'vms_app/shift_view.html', context)


# /////////////////// Transfer Register Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def transfer_register_view(request):
    transfers = TransferRegister.objects.all()
    context = {
        "menu": "menu-transfer-registry",
        "transfers": transfers
    }
    return render(request, 'vms_app/transfer_registry_list.html', context)


@login_required(login_url='login')
@active_required
def create_transfer_register(request):
    form = TransferRegisterForm()
    if request.method == 'POST':
        form = TransferRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transfer_register_view')
    context = {
        "form": form,
        "menu": "menu-transfer-registry",
        "form_title": "Add Transfer Register",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_transfer_register(request, id: int):
    transfer = TransferRegister.objects.get(id=id)
    form = TransferRegisterForm(instance=transfer)
    if request.method == 'POST':
        form = TransferRegisterForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return redirect('transfer_register_view')
    context = {
        "form": form,
        "menu": "menu-transfer-registry",
        "form_title": "Edit Transfer Register",
    }
    return render(request, 'vms_app/forms.html', context)


# /////////////////// Accident Log Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def accident_log_view(request):
    accidents = AccidentLog.objects.all()
    context = {
        "menu": "menu-accident-logs",
        "accidents": accidents
    }
    return render(request, 'vms_app/accident_log_list.html', context)


@login_required(login_url='login')
@active_required
def create_accident_log(request):
    form = AccidentLogForm()
    if request.method == 'POST':
        form = AccidentLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accident_log_view')
    context = {
        "form": form,
        "menu": "menu-accident-logs",
        "form_title": "Add Accident Log",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_accident_log(request, id: int):
    accident = AccidentLog.objects.get(id=id)
    form = AccidentLogForm(instance=accident)
    if request.method == 'POST':
        form = AccidentLogForm(request.POST, instance=accident)
        if form.is_valid():
            form.save()
            return redirect('accident_log_view')
    context = {
        "form": form,
        "menu": "menu-accident-logs",
        "form_title": "Edit Accident Log",
    }
    return render(request, 'vms_app/forms.html', context)


def testing_new(request):
    return render(request, 'vms_app/test.html', {})


# /////////////////// Workshop Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def workshop_list(request):
    workshop_list = Workshop.objects.all()
    context = {
        "menu": "menu-workshop",
        "workshop_list": workshop_list
    }
    return render(request, 'vms_app/workshop_list.html', context)


@login_required(login_url='login')
@active_required
def create_workshop(request):
    form = WorkshopForm()
    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workshop_list')
    context = {
        "form": form,
        "menu": "menu-workshop",
        "form_title": "New Workshop",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_workshop(request, id: int):
    workshop = Workshop.objects.get(id=id)
    form = WorkshopForm(instance=workshop)
    if request.method == 'POST':
        form = WorkshopForm(request.POST, instance=workshop)
        if form.is_valid():
            form.save()
            return redirect('workshop_list')
    context = {
        "form": form,
        "menu": "menu-workshop",
        "form_title": "Edit Workshop",
    }
    return render(request, 'vms_app/forms.html', context)


# /////////////////// Fuel Master Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def fuel_log_list(request):
    fuel_logs = FuelMaster.objects.all()

    context = {
        "fuel_logs": fuel_logs,
        "menu": "menu-fuel-log"
    }

    return render(request, 'vms_app/fuel_logs_list.html', context)


@login_required(login_url='login')
@active_required
def add_fuel_log(request):
    form = FuelMasterForm()
    if request.method == "POST":
        form = FuelMasterForm(request.POST)
        if form.is_valid():
            fuel_log = form.save()
            fuel_log.created_by = request.user
            return redirect('fuel_log_list')
        
    context = {
        "form": form,
        "menu": "menu-fuel-log",
        "form_title": "Add Fuel Log"
    }

    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_fuel_log(request, id):
    fuel_log = FuelMaster.objects.get(pk=id)
    form = FuelMasterForm(instance=fuel_log)
    if request.method == "POST":
        form = FuelMasterForm(request.POST, instance=fuel_log)
        if form.is_valid():
            log = form.save()
            log.updated_by = request.user

            return redirect('fuel_log_list')
        
    context = {
        "form": form,
        "menu": "menu-fuel-log",
        "form_title": "Edit Fuel Log"
    }

    return render(request, 'vms_app/forms.html', context)


def get_fuel_efficiency_data(vehicle_fuel_logs):
    total_fuel_quantity = vehicle_fuel_logs.aggregate(total_fuel_quantity=models.Sum('fuel_quantity'))['total_fuel_quantity']
    total_fuel_cost = round(vehicle_fuel_logs.aggregate(total_fuel_cost=models.Sum('fuel_cost'))['total_fuel_cost'], 2)
    first_fuel_log = vehicle_fuel_logs.first()
    last_fuel_log = vehicle_fuel_logs.last()
    average_mileage = round((last_fuel_log.fuel_km-first_fuel_log.fuel_km)/total_fuel_quantity, 2)
    return {
        "total_fuel_quantity": total_fuel_quantity, 
        "total_fuel_cost": total_fuel_cost, 
        "total_km": last_fuel_log.fuel_km, 
        "average_mileage": average_mileage
    }


@login_required(login_url='login')
@active_required
def fuel_efficieny_week_view(request):
    vehicles = Vehicle.objects.filter(is_active=True)
    fuel_efficiency_list = []
    for vehicle in vehicles:
        today = timezone.now()
        start_date = today - timezone.timedelta(days=today.weekday())
        end_date = start_date + timezone.timedelta(days=7)
        vehicle_fuel_logs = vehicle.vehicle_fuel_history.filter(
            fuel_date__gte=start_date,
            fuel_date__lte=end_date
        ).order_by("fuel_date")
        
        if len(vehicle_fuel_logs) > 1:
            fuel_efficiency_data = get_fuel_efficiency_data(vehicle_fuel_logs)
            fuel_efficiency_list.append({
                "vehicle": vehicle, 
                **fuel_efficiency_data
            })
    context = {
        "view_title": today.strftime("Week-%W %B %Y"),
        "fuel_logs": fuel_efficiency_list,
        "menu": "menu-fuel-log",
    }
    return render(request, 'vms_app/fuel_efficiency_list.html', context)


@login_required(login_url='login')
@active_required
def fuel_efficieny_month_view(request):
    vehicles = Vehicle.objects.filter(is_active=True)
    fuel_efficiency_list = []
    for vehicle in vehicles:
        today = timezone.now()
        current_year = today.year
        current_month = today.month
        vehicle_fuel_logs = vehicle.vehicle_fuel_history.filter(
            fuel_date__year=current_year,
            fuel_date__month=current_month
        ).order_by("fuel_date")
        
        if len(vehicle_fuel_logs) > 1:
            fuel_efficiency_data = get_fuel_efficiency_data(vehicle_fuel_logs)
            fuel_efficiency_list.append({
                "vehicle": vehicle, 
                **fuel_efficiency_data
            })
    context = {
        "view_title": today.strftime("%B %Y"),
        "fuel_logs": fuel_efficiency_list,
        "menu": "menu-fuel-log",
    }
    return render(request, 'vms_app/fuel_efficiency_list.html', context)


@login_required(login_url='login')
@active_required
def fuel_efficieny_custom_view(request):
    today = timezone.now()
    data = {
        "start": today,
        "end": today,
    }
    if request.method == "POST":
        form = CustomDateFilterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data

    vehicles = Vehicle.objects.filter(is_active=True)
    fuel_efficiency_list = []
    for vehicle in vehicles:
        vehicle_fuel_logs = vehicle.vehicle_fuel_history.filter(
            fuel_date__gte=data['start'],
            fuel_date__lte=data['end']
        ).order_by("fuel_date")
        
        if len(vehicle_fuel_logs) > 1:
            fuel_efficiency_data = get_fuel_efficiency_data(vehicle_fuel_logs)
            fuel_efficiency_list.append({
                "vehicle": vehicle, 
                **fuel_efficiency_data
            })
    context = {
        "view_title": "Custom Report",
        "fuel_logs": fuel_efficiency_list,
        "data": data,
        "menu": "menu-fuel-log",
    }
    return render(request, 'vms_app/fuel_efficiency_list.html', context)


# /////////////////// Job Card Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def job_card_list(request):
    job_cards = JobCard.objects.all()
    context = {
        "menu": "menu-job-card",
        "job_cards": job_cards
    }
    return render(request, 'vms_app/job_card_list.html', context)


@login_required(login_url='login')
@active_required
def add_job_card(request):
    form = JobCardForm()
    if request.method == "POST":
        form = JobCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_card_list')
    context = {
        "menu": "menu-job-card",
        "form": form,
        "form_title": "Add Job Card"
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_job_card(request, id):
    job_card = JobCard.objects.get(id=id)
    form = JobCardForm(instance=job_card)
    if request.method == "POST":
        form = JobCardForm(request.POST, instance=job_card)
        if form.is_valid():
            form.save()
            return redirect('job_card_list')
    context = {
        "menu": "menu-job-card",
        "form": form,
        "form_title": "Edit Job Card"
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def start_job_card(request, id):
    try:
        job_card = JobCard.objects.get(id=id)
        job_card.work_start_at = timezone.now()
        job_card.save()
    except JobCard.DoesNotExist:
        pass
    return redirect('job_card_list')


@login_required(login_url='login')
@active_required
def end_job_card(request, id):
    try:
        job_card = JobCard.objects.get(id=id)
        job_card.work_closed_at = timezone.now()
        job_card.save()
    except JobCard.DoesNotExist:
        pass
    return redirect('job_card_list')


@login_required(login_url='login')
@active_required
def vehicle_job_history(request):
    current_datetime = timezone.now()
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = start_of_month.replace(month=start_of_month.month + 1)
    end_of_month = next_month - timezone.timedelta(days=1)
    data = {
        "start": start_of_month,
        "end": end_of_month
    }

    if request.method == "POST":
        form = CustomDateFilterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data

    vehicles = Vehicle.objects.filter(is_active=True)
    vehicle_maintanence_history = []
    for vehicle in vehicles:
        vehicle_maintanence_log = vehicle.vehicle_maintanence_history.filter(
            work_start_at__gte=data['start'],
            work_start_at__lte=data['end']
        )

        vehicle_maintanence_history.append({
            "vehicle": vehicle,
            "total_count": len(vehicle_maintanence_log),
            "total_cost": vehicle_maintanence_log.aggregate(total_cost=Sum('cost'))['total_cost']
        })

    context = {
        "menu": "menu-job-card",
        "data": data,
        "vehicle_maintanence_history": vehicle_maintanence_history,
    }
    return render(request, 'vms_app/vehicle_job_history.html', context)


@login_required(login_url='login')
@active_required
def vehicle_maintanence_view(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle_maintanence_log = vehicle.vehicle_maintanence_history.all()
    context = {
        "menu": "menu-job-card",
        "vehicle": vehicle,
        "vehicle_maintanence_log": vehicle_maintanence_log
    }
    return render(request, 'vms_app/vehicle_maintanence_view.html', context)
