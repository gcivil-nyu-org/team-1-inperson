from django.db import models


# Create your models here.


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.email

class EditInfo(models.Model):
    new_first_name=models.CharField(max_length=200)
    # new_last_name = models.CharField(max_length=200)
    # new_password = models.CharField(max_length=200)