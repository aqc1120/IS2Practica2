from django.db import models
from django.urls import reverse

# Create your models here.
class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    ),
    popularity = models.IntegerField(default=0)  # Campo para indicar la popularidad
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("destination_detail", kwargs={"pk": self.pk})
    
class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )
    def __str__(self):
        return self.name

class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )
    class Opinion(models.Model):
        name = models.CharField(max_length=100)
        cruise = models.CharField(max_length=100)
        opinion = models.TextField()
        valoracion = models.IntegerField()
    def __str__(self):
        return f"{self.name} - {self.cruise}"