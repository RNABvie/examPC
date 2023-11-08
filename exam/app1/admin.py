from django.contrib import admin
from app1 import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.PostComments)
admin.site.register(models.Profile)