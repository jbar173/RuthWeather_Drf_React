from django.contrib import admin
from .models import Report,Am,Pm,Eve

# Register your models here.

admin.site.register(Report)
admin.site.register(Am)
admin.site.register(Pm)
admin.site.register(Eve)
