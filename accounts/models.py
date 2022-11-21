from django.db import models


# Create your models here.


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.email


class FNameChange(models.Model):
    new_first_name = models.CharField(max_length=200)

    def __str__(self):
        return self.new_first_name


class LNameChange(models.Model):
    new_last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.new_last_name


class PassWordChange(models.Model):
    new_password = models.CharField(max_length=200)

    def __str__(self):
        return self.new_password
