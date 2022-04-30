from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Branch(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return str(self.name)


class City(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return str(self.name)


class Company(AbstractUser):
    username = models.CharField(max_length=200, unique=True, null=True)
    company_name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.company_name:
            return str(self.company_name)
        return str(self.username)


class JobOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, default=4, null=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, default=1, null=True)

    position = models.TextField(null=True, blank=True)
    working_mode = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    min_salary = models.IntegerField(null=True)
    max_salary = models.IntegerField(null=True)
    currency = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.position)
