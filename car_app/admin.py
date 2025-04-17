from django.contrib import admin

from car_app.models import *

# Register your models here.
@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    list_editable = ('name',)  # removed 'id'
    search_fields = ('id', 'name')
    ordering = ('id', 'name')  
    actions = ['delete_selected']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'car_license', 'car_engine_number')
    list_display_links = ('name',)  # makes 'name' clickable instead of 'id'
    list_filter = ('car_license', 'car_engine_number')
    list_editable = ('phone', 'car_license', 'car_engine_number')  # editable inline
    search_fields = ('name', 'phone', 'car_license', 'car_engine_number', 'address')
    ordering = ('id', 'name')
    actions = ['delete_selected']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_date','mechanic','car_license')
    list_filter = ('id', 'appointment_date','mechanic','car_license')
    list_editable = ('appointment_date','mechanic','car_license',)  # removed 'id'
    search_fields = ('id', 'appointment_date','mechanic','car_license')
    ordering = ('id', 'appointment_date','mechanic','car_license')  
    actions = ['delete_selected']
