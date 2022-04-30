from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Company)
admin.site.register(models.JobOffer)
admin.site.register(models.Branch)
admin.site.register(models.City)
