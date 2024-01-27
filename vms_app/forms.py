from django import forms
from .models import Employee, Vehicle, Route, Productivity


class VehicleForm(forms.ModelForm):
    
    class Meta:
        model = Vehicle
        fields = ("vehicle_number", "is_active", "is_working", "supervisor", "remark")

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class RouteForm(forms.ModelForm):
    
    class Meta:
        model = Route
        fields = ("area", "block", "street", "is_active", "estimation")
