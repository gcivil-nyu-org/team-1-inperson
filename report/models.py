from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    reportID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    infraID = models.ForeignKey('landing_map.Accessible_location', on_delete = models.CASCADE)
    updatedAt = models.DateTimeField(auto_now = True)
    createdAt = models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length = 100, default = "")
    isResolved = models.BooleanField(default = False)
    dateTimeOfResolution = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return str(self.reportID)