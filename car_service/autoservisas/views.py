from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from . forms import OrderCommentForm, CarForm, OrderForm
from . models import CarModel, Car, Order, Service, OrderEntry

# Create your views here.

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    services_count = Service.objects.all().count()
    services_done = OrderEntry.objects.all().count()
    count_cars = Car.objects.all().count()
    
    # Apsilankymų skaitliukas
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'services_count': services_count,
        'services_done': services_done,
        'count_cars': count_cars,
        'num_visits': num_visits,
    }

    return render(request, 'autoservisas/index.html', context)

def car_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(plate_number__istartswith=query) |
            Q(car_model__make__icontains=query)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 3)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'autoservisas/cars_list.html', {
        'car_list': car_list,
    })

def car_detail(request, pk: int):
    return render(request, 'autoservisas/car_detail.html', {
        'car': get_object_or_404(Car, pk=pk)
    })


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 3
    template_name = 'autoservisas/order_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(date__istartswith=query) |
                Q(car__customer__icontains=query) |
                Q(car__plate_number__istartswith=query)
            )
        return qs


class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Order
    template_name = 'autoservisas/order_details.html'
    form_class = OrderCommentForm

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['commenter'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.commenter = self.request.user
        form.save()
        messages.success(self.request, _('Comment posted!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('order_details', kwargs={'pk':self.get_object().pk})


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'autoservisas/user_order_list.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__customer=self.request.user)
        return qs


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = 'autoservisas/car_form.html'
    success_url = reverse_lazy('user_car_list')

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['customer'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, _('Car Added!'))
        return super().form_valid(form)
        

class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'autoservisas/order_form.html'
    success_url = reverse_lazy('user_order_list')

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order_sum'] = 1
        return initial

    def form_valid(self, form):
        form.instance.order_sum = 1
        messages.success(self.request, _('Order Created!'))
        return super().form_valid(form)


class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'autoservisas/user_cars_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs


# class CarInfoUpdateView(
#     LoginRequiredMixin, 
#     UserPassesTestMixin, 
#     generic.UpdateView
# ):
#     model = Car
#     form_class = CarForm
#     template_name = 'autoservisas/user_cars_list.html'
#     success_url = reverse_lazy('user_car_list')

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         obj = self.get_object()
#         context['car'] = obj.car
#         if obj.status == 1:
#             context['changing'] = True
#         else:
#             context['extending'] = True
#         return context

#     def get_initial(self) -> Dict[str, Any]:
#         initial = super().get_initial()
#         initial['due_back'] = date.today() + timedelta(days=14)
#         initial['status'] = 2
#         return initial

#     def form_valid(self, form):
#         form.instance.reader = self.request.user
#         form.instance.status = 2
#         return super().form_valid(form)

#     def test_func(self) -> bool | None:
#         obj = self.get_object()
#         return obj.reader == self.request.user