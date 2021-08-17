from django.contrib import admin

# Register your models here.
from .models import *

from import_export.admin import ImportExportModelAdmin
@admin.register(Response,problem_detail)
class ViewAdmin(ImportExportModelAdmin):
    pass
