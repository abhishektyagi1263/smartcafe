from django.contrib import admin
from .models import User,Student
# Register your models here.

from import_export.admin import ImportExportModelAdmin
@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    pass
