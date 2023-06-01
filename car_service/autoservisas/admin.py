from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class CarAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'vin_code', 'customer', 'car_model')
    list_filter = ('customer', 'car_model')
    search_fields = ('plate_number', 'vin_code')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'engine', 'year')


class OrderEntryInline(admin.TabularInline):
    model = models.OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'order_sum', 'status')
    inlines = [OrderEntryInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'price', 'service')


admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry, OrderEntryAdmin)

# Register your models here.
