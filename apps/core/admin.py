from django.contrib import admin
from .models import Category, Job, JobApplication, Contact

admin.site.register(Category)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(Contact)
