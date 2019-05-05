from django.contrib import admin
from dashboard.models import User, Student, Activity, Entrylist

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Activity)
admin.site.register(Entrylist)