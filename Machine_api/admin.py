from django.contrib import admin
from .models import User, Machine, Organisation, Project

admin.site.register(User)
admin.site.register(Machine)
admin.site.register(Organisation)
admin.site.register(Project)
