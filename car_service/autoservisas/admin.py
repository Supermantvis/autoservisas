from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class CarAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'vin_code', 'car_model', 'customer')
    list_filter = ('customer', 'car_model')
    search_fields = ('plate_number', 'vin_code')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'engine', 'year')


class OrderEntryInline(admin.TabularInline):
    model = models.OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'order_sum', 'status', 'due_back')
    inlines = [OrderEntryInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'price', 'service')


class OrderCommentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'order', 'commenter', 'content')


admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry, OrderEntryAdmin)
admin.site.register(models.OrderComment, OrderCommentAdmin)

# Register your models here.
