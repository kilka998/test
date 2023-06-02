from rest_framework import serializers
from .models import Department, Employee
from django.db.models import Sum


class ReadOnlyDirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'id',
            'full_name',
        )


class ReadOnlyEmployeesDepartamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
        )


class ReadOnlyEmployeeSerializer(serializers.ModelSerializer):
    department = ReadOnlyEmployeesDepartamentSerializer(allow_null=True)

    class Meta:
        model = Employee
        fields = '__all__'


class ReadOnlyDepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    total_salary = serializers.SerializerMethodField()
    director = ReadOnlyDirectorSerializer(allow_null=True)


    class Meta:
        model = Department
        fields = '__all__'


    def get_employee_count(self, obj):
        # Тут можно было воспользоваться агрегацией по количеству
        # прицип тот же самый, что и ниже obj.employees.aggregate(cnt=Count('id'))['cnt']
        # но на мой взгляд это бессмысленно в данном случае)
        return obj.employees.count()

    def get_total_salary(self, obj):
        return obj.employees.aggregate(sum=Sum('salary'))['sum']


class CreateEmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee

        fields = (
            'full_name',
            'position',
            'salary',
            'age',
            'department',
        )
