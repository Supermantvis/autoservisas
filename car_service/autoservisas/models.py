from django.contrib.auth import get_user_model
from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()


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
    note = HTMLField(_("note"), max_length=4000, null=True, blank=True)
    car_model = models.ForeignKey(
        CarModel,
        verbose_name=_("car model"),
        on_delete=models.CASCADE,
        related_name="cars",
    )

    car_img = models.ImageField(
        _("car_img"),
        upload_to="autoservisas/car_images",
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        User,
        verbose_name=_("customer"),
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True
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

    due_back = models.DateField(_("due back"), null=True, blank=True, db_index=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    @property
    def customer(self):
        return self.car.customer

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
    quantity = models.DecimalField(_("quantity"), max_digits=18, decimal_places=2, default=1)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    total = models.DecimalField(_("total"), max_digits=18, decimal_places=2, default=0)
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
        return f"{self.service} {self.quantity} {self.price}"

    def get_absolute_url(self):
        return reverse("order_entry_detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.order_sum = self.order.order_entries.aggregate(models.Sum("total"))["total__sum"]
        self.order.save()


class OrderComment(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name='comments'
        )
    commenter = models.ForeignKey(User,
        verbose_name=_("commenter"),
        on_delete=models.SET_NULL,
        related_name='order_comments',
        null=True, blank=True,
        )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)    

    class Meta:
        ordering=['-created_at']
        verbose_name = _("order comment")
        verbose_name_plural = _("order comments")

    def __str__(self):
        return f"{self.created_at}: {self.commenter}"

    def get_absolute_url(self):
        return reverse("ordercomment_detail", kwargs={"pk": self.pk})
