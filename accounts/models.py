from django.db import models


# Create your models here.


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.email


class EditFName(models.Model):
    new_first_name = models.CharField(max_length=25)


class EditLName(models.Model):
    new_last_name = models.CharField(max_length=25)


class EditPassword(models.Model):
    new_password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
