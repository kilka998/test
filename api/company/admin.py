from django.contrib import admin
from .models import Department, Employee, UserToken

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    model = Department

    list_display = (
        'name',
        'director_name',
    )
    

    search_fields = (
        'name',
        'director__full_name',
    )

    def get_director_name(self, instance: Department):
        return instance.director_name 
    
    get_director_name.short_description = 'ФИО директора'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    model = Employee

    fields = (
        'full_name',
        'photo',
        'position',
        'salary',
        'age',
        'department',
        'token',
    )

    list_display = (
        'full_name',
        'position',
    )

    list_filter = (
        'position',
    )
    
    search_fields = (
        'full_name',
    )

    readonly_fields = (
        'token',
    )
    
    def token(self, instance: Employee):
        return token if (token := instance.get_token()) else instance.create_token()
    
    token.short_description = 'Токен'