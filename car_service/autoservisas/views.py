from django.http import HttpResponse
from django.shortcuts import render
from . models import CarModel, Car, Order, Service, OrderEntry

# Create your views here.

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    services_count = Service.objects.all().count()
    services_done = OrderEntry.objects.all().count()
    count_cars = Car.objects.all().count()
    
    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'services_count': services_count,
        'services_done': services_done,
        'count_cars': count_cars
    }

    return render(request, 'autoservisas/index.html', context)