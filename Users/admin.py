from django.contrib import admin
from . models import CustomUser,WastePickup,WasteReport
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(WasteReport)
admin.site.register(WastePickup)