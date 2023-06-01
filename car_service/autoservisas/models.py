from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CarModel(models.Model):
    make = models.CharField(_("make"), max_length=100)
    model = models.CharField(_("model"), max_length=100)
    engine = models.CharField(_("engine"), max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField(_("year"))

    class Meta:
        ordering = ["make"]
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.make} {self.model}"

    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})


class Car(models.Model):
    plate_number = models.CharField(_("plate number"), max_length=50)
    vin_code = models.CharField(_("vin code"), max_length=100)
    customer = models.CharField(_("customer"), max_length=100)
    car_model = models.ForeignKey(
        CarModel,
        verbose_name=_("car model"),
        on_delete=models.CASCADE,
        related_name="cars",
    )

    class Meta:
        ordering = ["car_model"]
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f"{self.plate_number} {self.vin_code} {self.customer} {self.car_model}"

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=True)
    order_sum = models.DecimalField(_("order sum"), max_digits=18, decimal_places=2, default=0)
    car = models.ForeignKey(
        Car,
        verbose_name=_("car"),
        on_delete=models.CASCADE,
        related_name="orders",
    )

    STATUS_CHOICES = (
        (0, _('Registered')),
        (1, _('Waiting')),
        (2, _('Being fixed')),
        (3, _('Fixed')),
        (4, _('Returned')),
        (5, _('Canceled')),
    )

    status = models.PositiveBigIntegerField(
        _("status"),
        choices=STATUS_CHOICES,
        default=0,
        db_index=True
    )

    class Meta:
        ordering = ["date", "id"]
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"{self.date} {self.order_sum} {self.car}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})



class Service(models.Model):
    name = models.CharField(_("name"), max_length=50)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return f"{self.name}, {self.price}"

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})


class OrderEntry(models.Model):
    amount = models.PositiveIntegerField(_("amount"), default=0)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    service = models.ForeignKey(
        Service,
        verbose_name=_("service"),
        on_delete=models.CASCADE,
        related_name="order_entries",
    )
    order = models.ForeignKey(
        Order,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name="order_entries",
    )

    class Meta:
        ordering = ["service"]
        verbose_name = _("order entry")
        verbose_name_plural = _("order entries")

    def __str__(self):
        return f"{self.amount}, {self.price}, {self.service}"

    def get_absolute_url(self):
        return reverse("order_entry_detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        super().save(*args, **kwargs)