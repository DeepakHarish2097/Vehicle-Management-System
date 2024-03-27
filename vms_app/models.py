import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db import transaction


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
    is_zonal_manager = models.BooleanField(default=False)
    is_mechanic = models.BooleanField(default=False)
    contact = models.CharField(max_length=255)
    address = models.TextField()
    remark = models.TextField(null=True, blank=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.name


class Workshop(models.Model):
    workshop_name = models.CharField(max_length=50)
    incharge = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.workshop_name


class Zone(models.Model):
    zone_name = models.CharField(max_length=50, unique=True)
    zone_code = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.zone_code:
            return self.zone_code
        else:
            return self.zone_name


class Ward(models.Model):
    ward_name = models.CharField(max_length=50, unique=True)
    ward_code = models.CharField(max_length=50, blank=True, null=True)  # should be altered to unique later
    zone = models.ForeignKey(Zone, related_name='contained_wards_set', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ward_name}"


class Route(models.Model):
    zone = models.ForeignKey(Zone, related_name='zone_routes_set', on_delete=models.PROTECT)
    ward = models.ForeignKey(Ward, related_name='ward_routes_set', on_delete=models.PROTECT)
    route = models.CharField(max_length=500, null=True, blank=True)
    starting_point = models.CharField(max_length=250, default=None, null=True, blank=True)
    km_estimation = models.IntegerField(null=True, blank=True, default=50)
    time_estimation = models.IntegerField(default=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_working = models.BooleanField(default=False)
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='route_supervised_by', limit_choices_to={'is_active': True})

    # OBJECT LOG
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='route_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='route_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.zone}, {self.ward}, {self.route}"


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=100, unique=True)  # register number
    is_active = models.BooleanField(default=True)
    is_working = models.BooleanField(default=False)
    is_spare = models.BooleanField(default=False)
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='vehicle_supervised_by', limit_choices_to={'is_active': True})
    current_route = models.ForeignKey(Route, related_name='routesofvehicle', on_delete=models.PROTECT, null=True,
                                      blank=True)
    zone = models.ForeignKey(Zone, related_name='zone_vehicles_set',
                             on_delete=models.PROTECT, null=True, blank=True)
    workshop = models.ForeignKey(Workshop, related_name='workshop_vehicles_set',
                                 on_delete=models.PROTECT, null=True, blank=True)

    load_estimation = models.IntegerField(default=1000)  # in kg
    remark = models.TextField(null=True, blank=True)

    # object log
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='vehicle_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='vehicle_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vehicle_number + str(self.supervisor)


class Vehicles_RTO_details(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, primary_key=True)
    chassis_number = models.CharField(max_length=50, null=True, blank=True)
    vehicle_model = models.CharField(max_length=50, null=True, blank=True)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    engine_number = models.CharField(max_length=50, null=True, blank=True)
    fc_date = models.DateField(null=True, blank=True)
    insurance = models.DateField(null=True, blank=True)
    puc = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.vehicle)


class Shift(models.Model):
    choices_shifts = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('Others', 'Others')
    ]
    vehicle = models.ForeignKey(Vehicle, related_name="vehicle_shift_set", on_delete=models.PROTECT,
                                limit_choices_to={'is_active': True, 'is_working': False}, null=False)
    shift_name = models.CharField(max_length=100, choices=choices_shifts)
    start_time = models.DateTimeField(auto_now_add=True)
    routes = models.ManyToManyField(Route, blank=False, limit_choices_to={'is_active': True, 'is_working': False})
    out_km = models.FloatField(null=True, blank=True, default=0.0)
    start_image = models.ImageField(null=True, blank=True, upload_to='shift_start/')
    driver = models.CharField(max_length=500, default='Vendor')
    shift_date = models.DateField(auto_now_add=True)
    # ------------------------------------------------------------
    end_time = models.DateTimeField(null=True, blank=True)  # used to check shift completed or not in view
    in_km = models.FloatField(null=True, blank=True, default=0.0)
    end_image = models.ImageField(null=True, blank=True, upload_to='shift_end/')
    shift_remark = models.TextField(null=True, blank=True)
    # ------------------------------------------------------------
    created_on = models.DateTimeField(auto_now_add=True)
    time_estimation = models.FloatField(default=0, editable=False)
    km_estimation = models.IntegerField(default=1, editable=False)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)  #
            if self.routes.exists():  # Check if routes exist
                total_time_estimation = 0
                total_km_estimation = 0
                for route in self.routes.all():
                    total_time_estimation += route.time_estimation
                    total_km_estimation += route.km_estimation
                self.time_estimation = total_time_estimation
                self.km_estimation = total_km_estimation

                # Update the instance with new estimations
                super().save(*args, **kwargs)

    # shift_time_efficiency = models.FloatField(null=True, blank=True) #total routes time estimation/ shift duration
    # shift_km_efficiency = models.FloatField(null=True, blank=True) #total km estimation of the routes covered/ (in-out km)
    # shift_load_efficiency = models.FloatField(null=True, blank=True) # avg of total trip efficiency of that shift

    def __str__(self) -> str:
        return f"{self.vehicle} {self.shift_name} {self.driver}"

    @property
    def shift_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        else:
            return None

    @property
    def shift_km(self):
        if self.out_km and self.in_km:
            return self.in_km - self.out_km
        else:
            return None

    @property
    def shift_total_load(self):
        trips = self.shift_trips_set.all()
        total_load = 0
        for trip in trips:
            total_load += trip.trip_load
        return total_load

    @property
    def shift_load_efficiency(self):
        total_load = self.shift_total_load
        trips = self.shift_trips_set.all()
        if trips:
            total_load_estimation = self.vehicle.load_estimation * len(trips)
            return 100 * total_load / total_load_estimation
        else:
            return None

    @property
    def shift_km_conflicts(self):
        try:
            if self.shift_km and self.routes:
                total_km_estimation = 0
                for route in self.routes.all():
                    total_km_estimation += route.km_estimation
                return self.shift_km / total_km_estimation
        except Exception as e:
            pass

        return None

    @property
    def shift_time_efficiency(self):
        try:
            if self.shift_duration and self.time_estimation:
                return 100 * self.time_estimation / (self.shift_duration.total_seconds() // 60)
        except Exception as e:
            return None

    @property
    def shit_total_time_estimation(self):
        if self.routes.all():
            time_estimation = 0
            for route in self.routes.all():
                time_estimation += route.time_estimation
            return time_estimation
        else:
            return 0

    @property
    def shift_km_estimation(self):
        if self.routes.all():
            km_estimation = 0
            for route in self.routes.all():
                km_estimation += route.km_estimation
            return km_estimation
        else:
            return 0

    @property
    def shit_total_trip_count(self):
        return len(self.shift_trips_set.all())

    class Meta:
        unique_together = ['shift_name', 'vehicle', 'shift_date']


class TripHistory(models.Model):
    choices_shifts = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('Others', 'Others')
    ]
    shift = models.ForeignKey(Shift, related_name='shift_trips_set', on_delete=models.CASCADE, null=False)
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle_trips_set', on_delete=models.PROTECT, null=False)
    is_current = models.BooleanField(default=True, editable=False)
    trip_date = models.DateField(auto_now_add=True)
    trip_start_time = models.DateTimeField(auto_now_add=True)
    updted_on = models.DateTimeField(auto_now=True)
    trip_end_time = models.DateTimeField(null=True, blank=True)

    wet_waste = models.IntegerField(default=0)
    recyclable_waste = models.IntegerField(default=0)
    dry_waste = models.IntegerField(default=0)
    inerts = models.IntegerField(default=0)
    household_hazard = models.IntegerField(default=0)
    green_garbages = models.IntegerField(default=0)
    other_waste = models.IntegerField(default=0)
    total_trip_load = models.IntegerField(null=True, blank=True)  # in kg # set it as property
    trip_remark = models.TextField(null=True, blank=True)
    # Method Fields set by overwriting save method
    trip_count = models.IntegerField(default=0)  # method field have to be increased +1 in backend
    trip_efficiency = models.FloatField(default=0)

    @property
    def total_trip_load(self):
        total_trip_load = (self.wet_waste + self.recyclable_waste + self.dry_waste
                           + self.inerts + self.household_hazard + self.green_garbages + self.other_waste)
        return total_trip_load

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.trip_count == 0:
            existing_trips = TripHistory.objects.filter(shift=self.shift, vehicle=self.vehicle,
                                                        trip_date=self.trip_date)
            print(existing_trips, len(existing_trips))
            self.trip_count = len(existing_trips) + 1
        if self.total_trip_load:
            self.trip_efficiency = self.trip_load / self.vehicle.load_estimation
        super().save(*args, **kwargs)
        # self.save(update_fields=['trip_load', 'trip_count'])


class TransferRegister(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    request_date = models.DateField()
    from_zone = models.ForeignKey(Zone, related_name='from_zones_tl', on_delete=models.PROTECT)
    to_zone = models.ForeignKey(Zone, related_name='to_zones_tl', on_delete=models.PROTECT)
    requested_by = models.ForeignKey(Employee, related_name='emp_requests_set', on_delete=models.PROTECT)
    reason = models.TextField()

    approved_date = models.DateField(null=True, blank=True, default=None)
    approved_by = models.ForeignKey(Employee, related_name='emp_responds', on_delete=models.PROTECT,
                                    null=True, blank=True)
    status = models.CharField(max_length=100, choices=[
        ('approved', 'approved'), ('hold', 'hold'), ('rejected', 'rejected')
    ])
    # approver remark
    remark = models.CharField(max_length=250, null=True, blank=True)
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


class FuelMaster(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle_fuel_history', on_delete=models.PROTECT,
                                limit_choices_to={'is_active': True})
    fuel_choices = [
        ('P', 'Petrol'),
        ('D', 'Diesel'),
        ('G', 'Gas')
    ]
    fuel_type = models.CharField(max_length=1, choices=fuel_choices)
    fuel_km = models.FloatField(null=True, blank=True)
    fuel_date = models.DateField(null=True, blank=True)
    fuel_quantity = models.FloatField(default=1)
    fuel_cost = models.FloatField(default=102.6)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='employee_fuel_history')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='employee_fuelupdate_history')
    updated_on = models.DateTimeField(auto_now=True)


class MaintenanceSchedules(models.Model):
    '''
    Model objectives:
    Have list the history of service done for evey vehicles
    Have to list the vehicles who are missed thier date
    Have to check the km gap between services 
    user display table should have only pending status. The admin can see get all queryset
    The display table should have two colors to discriminate overdue and normal
    By clicking the vehicle in table should lead to schedule history of the vehicle.
    '''
    service_choices = [('SS1 WITH ENGINE OIL & FILTER', 'SS1 WITH ENGINE OIL & FILTER'),
                       ('SS Gen WITHOUT ENGINE OIL & FILTER', 'SS Gen WITHOUT ENGINE OIL & FILTER'),
                       ('SS2', 'SS2'), ('SS3', 'SS3'), ('SS4', 'SS4')]

    vehicle = models.ForeignKey(Vehicle, related_name='vehicle_shcedule_history',
                                on_delete=models.PROTECT, limit_choices_to={'is_active': True})
    odo_closing = models.FloatField(default=0)
    service = models.CharField(max_length=250, choices=service_choices)
    scheduled_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Done', 'Done'), ('Pending', 'Pending')])


class JobCard(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle_maintanence_history',
                                on_delete=models.PROTECT, limit_choices_to={'is_active': True})
    workshop = models.ForeignKey(Workshop, related_name='workshop_jobs',
                                 on_delete=models.PROTECT)
    assigned_on = models.DateTimeField(auto_now_add=True)
    work_start_at = models.DateTimeField(null=True, blank=True)
    work_closed_at = models.DateTimeField(null=True, blank=True)
    work = models.CharField(max_length=250, blank=True, null=True)
    zonal_manager_remark = models.TextField(null=True, blank=True)
    spares = models.CharField(max_length=500, blank=True, null=True)
    cost = models.FloatField(null=True, blank=True)
    mechanics = models.CharField(max_length=500, blank=True, null=True)
    driver = models.CharField(max_length=500, blank=True, null=True)
    remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50,
                              choices=[('Assigned', 'Assigned'), ('Working', 'Working'), ('Completed', 'Completed')],
                              default="Assigned")
