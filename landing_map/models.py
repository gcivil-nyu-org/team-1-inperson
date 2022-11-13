from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Infra_type(models.Model):
    typeID = models.IntegerField(primary_key=True)
    typeName = models.CharField(max_length=20)

    def __str__(self):
        return self.typeName


class Favorite(models.Model):
    class Meta:
        unique_together = (("userID"), ("locationX"), ("locationY"))

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    locationX = models.CharField(max_length=22)
    locationY = models.CharField(max_length=22)
    address = models.CharField(max_length=100, default="")


class Accessible_location(models.Model):
    infraID = models.IntegerField(primary_key=True)
    locationX = models.CharField(max_length=22)
    locationY = models.CharField(max_length=22)
    typeID = models.ForeignKey(Infra_type, on_delete=models.PROTECT)
    isAccessible = models.BooleanField(default=True)
    street1 = models.CharField(max_length=20, default=None)
    street2 = models.CharField(max_length=20, default=None)
    borough = models.CharField(max_length=15, default=None)
    address = models.CharField(max_length=200, default=None)

    def __str__(self):
        return (
            str(self.infraID)
            + " "
            + str(self.locationX)
            + " "
            + str(self.locationY)
            + " "
            + str(self.typeID)
            + " "
            + str(self.isAccessible)
        )
