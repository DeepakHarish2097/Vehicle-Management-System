from django import forms
from .models import Employee, Vehicle, Route, Productivity
from django.contrib.auth.forms import UserCreationForm


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


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
        fields = ("street", "supervisor", "estimation")


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
        fields = ['vehicle', 'start', 'routes', 'driver']
        widgets = {
            'start': DateTimeInput()
        }


class ProductivityReportForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()
