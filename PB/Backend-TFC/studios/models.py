from django.db import models
from django.core.validators import MinValueValidator 
from django.db.models import CASCADE

class Studio(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length = 100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, blank=False, default = 0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, blank=False, default = 0)
    postal_code = models.CharField(max_length = 7)
    phone_number = models.CharField(max_length = 15)
    distance = models.CharField(max_length = 40, null=True, blank=True, default = 0)


    def __str__(self):
        return self.name

class Image(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='Image')
    image = models.ImageField(upload_to='studio_images/', blank=False, default=None)

    def __str__(self):
        return self.studio.name

class Amenities(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='Ammenity')
    type = models.CharField(max_length = 30, blank=False, default=None)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['studio', 'type'], name="unique_type"),
         ]

    def __str__(self):
        return self.studio.name
