from django import forms
from .models import Employee, Vehicle, Route, Productivity, Zone, Ward, \
    TransferRegister, AccidentLog, Shift
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput, TimeInput


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ["is_working", "created_by", "created_on", "updated_by", "updated_on"]
        widgets = {
            'fc_date': DateInput(attrs={'type': 'date'}),
            'insurance': DateInput(attrs={'type': 'date'}),
            'puc': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = "__all__"


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = "__all__"


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("zone", "ward", "street", "supervisor", "time_estimation", "km_estimation")


class EmployeeRegistrationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'password1', 'password2', 'contact', 'address', 'remark']

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': '3'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'image', 'contact', 'address', 'remark']

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': '3'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class ProductivityForm(forms.ModelForm):
    class Meta:
        model = Productivity
        fields = ['shift', 'vehicle', 'start', 'out_km', 'routes', 'driver', 'start_image']
        widgets = {
            'start': DateTimeInput()
        }


class ProductivityEndForm(forms.ModelForm):
    class Meta:
        model = Productivity
        fields = ['trip_ton', 'in_km', 'end_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trip_ton'].required = True
        self.fields['in_km'].required = True
        self.fields['end_image'].required = True


class ProductivityReportForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['shift_name', 'vehicle', 'start', 'out_km', 'routes', 'driver', 'start_image']
        widgets = {
            'start': DateTimeInput()
        }


class ShiftEndForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['trip_ton', 'in_km', 'end_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trip_ton'].required = True
        self.fields['in_km'].required = True
        self.fields['end_image'].required = True


class ShiftReportForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()


class TransferRegisterForm(forms.ModelForm):
    class Meta:
        model = TransferRegister
        fields = '__all__'
        widgets = {
            'transfer_date': DateInput(attrs={'type': 'date'}),
        }


class AccidentLogForm(forms.ModelForm):
    class Meta:
        model = AccidentLog
        fields = '__all__'
        widgets = {
            'accident_time': DateTimeInput()
        }
