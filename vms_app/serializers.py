from rest_framework import serializers

from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class ProductivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Productivity
        fields = '__all__'


class TransferRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRegister
        fields = '__all__'


class AccidentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccidentLog
        fields = '__all__'
