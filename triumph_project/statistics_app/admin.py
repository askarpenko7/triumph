from django.contrib import admin

# Register your models here.
from .models import Session, StudentAnswer

admin.site.register(Session)
admin.site.register(StudentAnswer)
