from django.contrib import admin
from .models import *

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(Todo, TodoAdmin)
