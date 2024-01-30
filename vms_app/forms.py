from django import forms
from .models import Employee, Vehicle, Route, Productivity
from django.contrib.auth.forms import UserCreationForm


class VehicleForm(forms.ModelForm):
    
    class Meta:
        model = Vehicle
        fields = ("vehicle_number", "supervisor", "remark")

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class RouteForm(forms.ModelForm):
    
    class Meta:
        model = Route
        fields = ("area", "block", "street", "estimation")


class EmployeeRegistrationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'password1', 'password2', 'contact', 'address', 'remark']

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': '3'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})
