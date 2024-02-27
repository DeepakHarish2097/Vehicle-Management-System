from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employee, Vehicle, Route, Productivity, Zone, Ward, \
    TransferRegister, AccidentLog, Shift
from .models import *
from .forms import VehicleForm, RouteForm, EmployeeRegistrationForm, \
    ProductivityForm, ProductivityReportForm, EmployeeEditForm, ZoneForm, \
    WardForm, TransferRegisterForm, AccidentLogForm, ProductivityEndForm, \
    ShiftForm, ShiftEndForm, ShiftReportForm
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
    shift = Shift.objects.filter(start__date=timezone.now().date())
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
            shift = form.save(commit=False)
            total_time_estimation = 0
            total_km_estimation = 0
            for route in clean_data['routes']:
                total_time_estimation += route.time_estimation
                total_km_estimation += route.km_estimation
                route.is_working = True
                route.save()
            shift.time_estimation = total_time_estimation
            shift.km_estimation = total_km_estimation
            current_shift = shift.save()
            vehicle = shift.vehicle
            vehicle.is_working = True
            vehicle.save()
            # TripHistory operations
            trip = TripHistory()
            trip.shift = current_shift
            trip.vehicle=vehicle
            trip.save()
            # trip.is_current will be set True by default. We have off it while rotating the shift
            # trip_count will save by overwritten save method in models.py
            shift.routes.set(clean_data['routes'])
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
def rotate_trip(request, id: int): # We gave to use the trip object id now
    trip = TripHistory.objects.get(pk=id)
    shift = trip.shift
    form = RotateTripForm()
    if request.method == "POST":
        form = RotateTripForm(request.POST, instance=trip)
        if form.is_valid():
            trip_obj = form.save(commit=False)
            trip_obj.is_current=False
            trip_obj.trip_end_time = datetime.datetime.now()
            trip_obj.save()
            # trip_efficiency will be save by overwritten save method in models.py
            
            # Starting next trip
            next_trip = TripHistory()
            next_trip.shift = shift
            next_trip.vehicle=shift.vehicle
            next_trip.save()
        else:
            return HttpResponse('Form invalid')



  
                
            # end def
            

        
    return redirect('shift_list')


# @login_required(login_url='login')
# @active_required
# def end_shift(request, id: int):
#     shift = Shift.objects.get(pk=id)
#     form = ShiftEndForm(instance=shift)

#     if request.method == "POST":
#         trip_ton = int(request.POST.get("trip_ton", 0))
#         form = ShiftEndForm(request.POST, request.FILES, instance=shift)
#         if form.is_valid():
#             shift = form.save(commit=False)
#             if shift.total_trip == 1:
#                 shift.first_trip_ton = trip_ton
#             elif shift.total_trip == 2:
#                 shift.second_trip_ton = trip_ton
#             elif shift.total_trip == 3:
#                 shift.third_trip_ton = trip_ton
#             elif shift.total_trip == 4:
#                 shift.fourth_trip_ton = trip_ton
#             elif shift.total_trip == 5:
#                 shift.fifth_trip_ton = trip_ton
#             else:
#                 shift.sixth_trip_ton = trip_ton

#             shift.end = timezone.now()
#             shift.day_production = round((timezone.now() - shift.start).total_seconds() / 60)
#             shift.save()
#             vehicle = shift.vehicle
#             vehicle.is_working = False
#             vehicle.save()
#             for route in shift.routes.all():
#                 route.is_working = False
#                 route.save()
#             return redirect('shift_list')

#     context = {
#         "form": form,
#         "menu": "menu-shift",
#         "form_title": "End Shift",
#     }
#     return render(request, 'vms_app/forms.html', context)


# /////////////////// Productivity Views \\\\\\\\\\\\\\\\\\\
@login_required(login_url='login')
@active_required
def productivity_list(request):
    productivity = Productivity.objects.filter(start__date=timezone.now().date())
    query = request.GET.get("query", None)
    type = request.GET.get("type", None)

    if type and query:
        today_productivity = Productivity.objects.filter(start__date=timezone.now().date())
        if type == "production":
            if query == "highest":
                productivity = today_productivity.order_by('-day_production')
            elif query == "least":
                productivity = today_productivity.order_by('day_production')
            else:
                productivity = Productivity.objects.all()
        elif type == "estimation":
            if query == "highest":
                productivity = today_productivity.order_by('-estimation')
            else:
                productivity = today_productivity.order_by('estimation')
        else:
            if query == "unused":
                all_vehicles = Vehicle.objects.filter(is_active=True)
                prod_vehicles = Vehicle.objects.filter(vehicle_productivity_set__start__date__gte=timezone.now().date())
                productivity = [i for i in all_vehicles if i not in prod_vehicles]

    context = {
        "menu": "menu-productivity",
        "productivity_list": productivity,
        "type": type,
    }
    return render(request, 'vms_app/productivity_list.html', context)


@login_required(login_url='login')
@active_required
def add_productivity(request):
    form = ProductivityForm()

    if not request.user.is_superuser:
        vehicle = Vehicle.objects.filter(supervisor=request.user, is_working=False)
        routes = Route.objects.filter(supervisor=request.user)

        form.fields['vehicle'].queryset = vehicle
        form.fields['routes'].queryset = routes

    else:
        form.fields['vehicle'].queryset = Vehicle.objects.filter(is_working=False)
        form.fields['routes'].queryset = Route.objects.all()

    if request.method == "POST":
        form = ProductivityForm(request.POST, request.FILES)
        if form.is_valid():
            clean_data = form.cleaned_data
            productivity = form.save(commit=False)
            total_estimation = 0
            for route in clean_data['routes']:
                total_estimation += route.estimation
            productivity.estimation = total_estimation
            productivity.save()
            vehicle = productivity.vehicle
            vehicle.is_working = True
            vehicle.save()
            productivity.routes.set(clean_data['routes'])
            return redirect('productivity_list')

    context = {
        "form": form,
        "menu": "menu-productivity",
        "form_title": "Start Shift",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def edit_productivity(request, id: int):
    productivity = Productivity.objects.get(pk=id)
    vehicle = productivity.vehicle
    vehicle.is_working = False
    vehicle.save()
    form = ProductivityForm(instance=productivity)

    if not request.user.is_superuser:
        vehicle = Vehicle.objects.filter(supervisor=request.user, is_working=False)
        routes = Route.objects.filter(supervisor=request.user)

        form.fields['vehicle'].queryset = vehicle
        form.fields['routes'].queryset = routes

    if request.method == "POST":
        form = ProductivityForm(request.POST, request.FILES, instance=productivity)
        if form.is_valid():
            clean_data = form.cleaned_data
            productivity = form.save(commit=False)
            total_estimation = 0
            for route in clean_data['routes']:
                total_estimation += route.estimation
            productivity.estimation = total_estimation
            productivity.save()
            vehicle = productivity.vehicle
            vehicle.is_working = True
            vehicle.save()
            productivity.routes.set(clean_data['routes'])
            return redirect('productivity_list')

    context = {
        "form": form,
        "menu": "menu-productivity",
        "form_title": "Edit Shift",
    }
    return render(request, 'vms_app/forms.html', context)


@login_required(login_url='login')
@active_required
def end_productivity(request, id: int):
    productivity = Productivity.objects.get(pk=id)
    form = ProductivityEndForm(instance=productivity)

    if request.method == "POST":
        trip_ton = int(request.POST.get("trip_ton", 0))
        form = ProductivityEndForm(request.POST, request.FILES, instance=productivity)
        if form.is_valid():
            productivity = form.save(commit=False)
            if productivity.total_trip == 1:
                productivity.first_trip_ton = trip_ton
            elif productivity.total_trip == 2:
                productivity.second_trip_ton = trip_ton
            elif productivity.total_trip == 3:
                productivity.third_trip_ton = trip_ton
            elif productivity.total_trip == 4:
                productivity.fourth_trip_ton = trip_ton
            elif productivity.total_trip == 5:
                productivity.fifth_trip_ton = trip_ton
            else:
                productivity.sixth_trip_ton = trip_ton

            productivity.end = timezone.now()
            productivity.day_production = round((timezone.now() - productivity.start).total_seconds() / 60)
            productivity.save()
            vehicle = productivity.vehicle
            vehicle.is_working = False
            vehicle.save()
            return redirect('productivity_list')

    context = {
        "form": form,
        "menu": "menu-productivity",
        "form_title": "End Shift",
    }
    return render(request, 'vms_app/forms.html', context)


def productivity_excel_report(filename, productivity):
    wb = Workbook()
    ws = wb.active
    ws.title = filename

    headers = ["Vehicle No.", "Start", "End", "Driver", "Estimation", "Production"]
    ws.append(headers)

    for i in productivity:
        ws.append(
            [i.vehicle.vehicle_number, i.start.strftime('%d/%m/%Y'), i.end.strftime('%d/%m/%Y'), i.driver, i.estimation,
             i.day_production])

    return wb


@login_required(login_url='login')
@active_required
def productivity_week_report(request):
    today = timezone.now()
    start_date = today - timezone.timedelta(days=today.weekday())
    end_date = start_date + timezone.timedelta(days=7)
    filename = today.strftime("Week-%W %B %Y")
    productivity = Productivity.objects.filter(
        start__date__gte=start_date,
        start__date__lte=end_date
    )

    if request.method == "POST":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

        excel_report = productivity_excel_report(filename, productivity)
        excel_report.save(response)
        return response

    context = {
        "head": filename,
        "menu": "menu-productivity",
        "productivity_list": productivity
    }
    return render(request, 'vms_app/productivity_report.html', context)


@login_required(login_url='login')
@active_required
def productivity_month_report(request):
    today = timezone.now()
    current_year = today.year
    current_month = today.month
    productivity = Productivity.objects.filter(
        start__year=current_year,
        start__month=current_month
    )
    filename = today.strftime("%B %Y")

    if request.method == "POST":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

        excel_report = productivity_excel_report(filename, productivity)
        excel_report.save(response)
        return response

    context = {
        "head": filename,
        "menu": "menu-productivity",
        "productivity_list": productivity
    }
    return render(request, 'vms_app/productivity_report.html', context)


@login_required(login_url='login')
@active_required
def productivity_custom_report(request):
    today = timezone.now()
    data = {
        "start": today,
        "end": today,
    }
    download = False

    if request.method == "POST":
        download = bool(request.POST.get('download', False))
        form = ProductivityReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

    productivity = Productivity.objects.filter(
        start__date__gte=data['start'],
        start__date__lte=data['end']
    )

    if download:
        filename = f"{data['start'].strftime('%d.%m.%Y')} - {data['end'].strftime('%d.%m.%Y')}"
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

        excel_report = productivity_excel_report(filename, productivity)
        excel_report.save(response)
        return response

    context = {
        "data": data,
        "head": "Custom Report",
        "menu": "menu-productivity",
        "productivity_list": productivity,
        "custom": True
    }
    return render(request, 'vms_app/productivity_report.html', context)


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
