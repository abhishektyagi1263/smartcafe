from django.contrib import admin
from . import models

from import_export.admin import ImportExportModelAdmin

@admin.register(models.feedback)
class ViewAdmin(ImportExportModelAdmin):
    pass
