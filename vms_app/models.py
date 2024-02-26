import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class EmployeeManager(BaseUserManager):
    def create_user(self, employee_id, name, password=None, **extra_fields):
        if not employee_id:
            raise ValueError('The employee_id field must be set')
        user = self.model(employee_id=employee_id, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(employee_id, name, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    employee_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    contact = models.CharField(max_length=255)
    address = models.TextField()
    remark = models.TextField(null=True, blank=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.name


# =======================================Hasan 20240217========================================

class Workshop(models.Model):
    workshop_name = models.CharField(max_length=50)
    incharge = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.workshop_name


class Zone(models.Model):
    zone_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.zone_name


class Ward(models.Model):
    ward_name = models.CharField(max_length=50, unique=True)
    zone = models.ForeignKey(Zone, related_name='contained_wards_set', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ward_name}"


# -----------------------------------------------------------------------------------------------


class Route(models.Model):
    zone = models.ForeignKey(Zone, related_name='zone_routes_set', on_delete=models.PROTECT)
    ward = models.ForeignKey(Ward, related_name='ward_routes_set', on_delete=models.PROTECT)
    street = models.CharField(max_length=500)
    km_estimation = models.IntegerField(null=True, blank=True, default=50)
    time_estimation = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_working = models.BooleanField(default=False)
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='route_supervised_by', limit_choices_to={'is_active': True})
    # estimation = models.IntegerField()
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='route_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='route_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.zone}, {self.ward}, {self.street}"


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_working = models.BooleanField(default=False)
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='vehicle_supervised_by', limit_choices_to={'is_active': True})
    load_estimation = models.IntegerField(default=1000) #in kg
    remark = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='vehicle_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='vehicle_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    # ===========================Hasan 20240217 ===============================================
    zone = models.ForeignKey(Zone, related_name='zone_vehicles_set',
                             on_delete=models.PROTECT, null=True, blank=True)
    workshop = models.ForeignKey(Workshop, related_name='workshop_vehicles_set',
                                 on_delete=models.PROTECT, null=True, blank=True)

    # vehicle RTO details
    register_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    chassis_number = models.CharField(max_length=50, null=True, blank=True)
    vehicle_model = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    engine_number = models.CharField(max_length=50, null=True, blank=True)
    fc_date = models.DateField(null=True, blank=True)
    insurance = models.DateField(null=True, blank=True)
    puc = models.DateField(null=True, blank=True)  # pollution under control certificate expiry date

    # -----------------------------------------------------------------------------------------------

    def __str__(self) -> str:
        return self.vehicle_number


class Productivity(models.Model):
    choices_shifts = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('Others', 'Others')
    ]
    vehicle = models.ForeignKey(Vehicle, related_name="vehicle_productivity_set", on_delete=models.PROTECT,
                                limit_choices_to={'is_active': True, 'is_working': False})
    start = models.DateTimeField(default=timezone.now)
    out_km = models.FloatField(null=True, blank=True, default=0.0)
    start_image = models.ImageField(upload_to='productivity_start/')
    end = models.DateTimeField(null=True, blank=True)
    in_km = models.FloatField(null=True, blank=True, default=0.0)
    end_image = models.ImageField(upload_to='productivity_end/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)
    shift = models.CharField(max_length=100, choices=choices_shifts)
    routes = models.ManyToManyField(Route, blank=False, limit_choices_to={'is_active': True})
    estimation = models.IntegerField(null=True, blank=True)
    driver = models.CharField(max_length=500, default='Vendor')
    day_production = models.IntegerField(null=True, blank=True)
    total_trip = models.IntegerField(null=True, blank=True, default=1)
    first_trip_ton = models.IntegerField(null=True, blank=True)
    second_trip_ton = models.IntegerField(null=True, blank=True)
    third_trip_ton = models.IntegerField(null=True, blank=True)
    fourth_trip_ton = models.IntegerField(null=True, blank=True)
    fifth_trip_ton = models.IntegerField(null=True, blank=True)
    sixth_trip_ton = models.IntegerField(null=True, blank=True)
    trip_ton = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.vehicle}] {self.driver}"

    @property
    def conflict(self):
        if self.estimation and self.day_production:
            return (abs(self.estimation - self.day_production) / self.estimation) * 100
        else:
            return

    @property
    def total_ton(self):
        total_ton = self.first_trip_ton + self.second_trip_ton + self.third_trip_ton + self.fourth_trip_ton + \
                    self.fifth_trip_ton + self.sixth_trip_ton
        return total_ton
    
    class Meta:
        unique_together = ['shift', 'vehicle', 'created_date']


class Shift(models.Model):
    choices_shifts = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('Others', 'Others')
    ]
    vehicle = models.ForeignKey(Vehicle, related_name="vehicle_shift_set", on_delete=models.PROTECT,
                                limit_choices_to={'is_active': True, 'is_working': False})
    start = models.DateTimeField(default=timezone.now)
    out_km = models.FloatField(null=True, blank=True, default=0.0)
    start_image = models.ImageField(upload_to='shift_start/')
    end = models.DateTimeField(null=True, blank=True)
    in_km = models.FloatField(null=True, blank=True, default=0.0)
    end_image = models.ImageField(upload_to='shift_end/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)
    shift_name = models.CharField(max_length=100, choices=choices_shifts)
    routes = models.ManyToManyField(Route, blank=False, limit_choices_to={'is_active': True})
    time_estimation = models.IntegerField(null=True, blank=True)
    km_estimation = models.IntegerField(null=True, blank=True)
    driver = models.CharField(max_length=500, default='Vendor')
    day_production = models.IntegerField(null=True, blank=True)
    total_trip = models.IntegerField(null=True, blank=True, default=1)
    first_trip_ton = models.IntegerField(null=True, blank=True)
    second_trip_ton = models.IntegerField(null=True, blank=True)
    third_trip_ton = models.IntegerField(null=True, blank=True)
    fourth_trip_ton = models.IntegerField(null=True, blank=True)
    fifth_trip_ton = models.IntegerField(null=True, blank=True)
    sixth_trip_ton = models.IntegerField(null=True, blank=True)
    trip_ton = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.vehicle}] {self.driver}"

    @property
    def conflict(self):
        if self.estimation and self.day_production:
            return (abs(self.estimation - self.day_production) / self.estimation) * 100
        else:
            return

    @property
    def total_ton(self):
        total_ton = self.first_trip_ton + self.second_trip_ton + self.third_trip_ton + self.fourth_trip_ton + \
                    self.fifth_trip_ton + self.sixth_trip_ton
        return total_ton
    
    class Meta:
        unique_together = ['shift_name', 'vehicle', 'created_date']


# =================================== Hasan 20240217 ==============================================
class TransferRegister(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    transfer_date = models.DateField()
    from_zone = models.ForeignKey(Zone, related_name='from_zones_tl', on_delete=models.PROTECT)
    to_zone = models.ForeignKey(Zone, related_name='to_zones_tl', on_delete=models.PROTECT)
    requested_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
    reason = models.TextField()
    log_no = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle}({self.from_zone} -> {self.to_zone})"


class AccidentLog(models.Model):
    choices_accident_severity = [
        ('Fatality', 'Fatality'),
        ('Near Miss', 'Near Miss'),
        ('Property Damage', 'Property Damage')
    ]
    choices_causes = [
        ('Mechanical Failure', 'Mechanical Failure'),
        ('Hydraulic Failure', 'Hydraulic Failure'),
        ('Over Speeding', 'Over Speeding'),
        ('Poor Visibility', 'Poor Visibility'),
        ('Lack of Attention', 'Lack of Attention'),
        ('Influence of Alcohol', 'Influence of Alcohol'),
        ('Lack of Training', 'Lack of Training'),
        ('Others', 'Others')
    ]
    driver_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    employee_id = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    accident_time = models.DateTimeField(null=True, blank=True)
    accident_location = models.CharField(max_length=250, null=True, blank=True)
    accident_severity = models.CharField(max_length=100, choices=choices_accident_severity)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    cause_of_accident = models.CharField(max_length=100, choices=choices_causes)
    action_needed = models.TextField()
    remark = models.TextField()


class IncidentLog(models.Model):
    IncidentTypesChoices = [('Accident', 'Accident'), ('Breakdown', 'Breakdown'),
                            ('General Maintenance', 'General Maintenance')]
    incident_type = models.CharField(max_length=100, choices=IncidentTypesChoices)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    driver_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    employee_id = models.CharField(max_length=50, null=True, blank=True)
    driver_contact = models.CharField(max_length=50, null=True, blank=True)
    incident_time = models.DateTimeField(null=True, blank=True)
    incident_location = models.CharField(max_length=250, null=True, blank=True)
    incident_brief = models.TextField()
    cause_of_incident = models.TextField()
    investigated_by = models.CharField(max_length=200, null=True, blank=True)
    driver_comment = models.TextField()
    zonal_manager_comment = models.TextField()
    mechanic_comment = models.TextField()
    estimated_repair_cost = models.FloatField(null=True, blank=True)
    cost_responsible = models.CharField(max_length=250, choices=[('Company', 'Company'), ('Insurance', 'Insurance'),
                                                                 ('Third party', 'Third party')])
    sent_to = models.ForeignKey(Workshop, related_name='workshops_incidents_set', on_delete=models.PROTECT, null=True,
                                blank=True)
    action_needed = models.TextField()
    remark = models.TextField()

# class MaintenanceHistory(models.Model):
#     pass


class TripHistory(models.Model):
    choices_shifts = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('Others', 'Others')
    ]
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle_trips_set', on_delete=models.PROTECT)
    trip_date = models.DateField()
    shift = models.CharField(max_length=20, choices=choices_shifts)
    trip_count=models.IntegerField()
    trip_load = models.IntegerField() #in kg
    trip_efficiency = models.FloatField(default=0)
    trip_start_time = models.DateTimeField(auto_now_add=True)
    updted_on = models.DateTimeField(auto_now=True)
    trip_end_time=models.DateTimeField(null=True, blank=True)

    
    