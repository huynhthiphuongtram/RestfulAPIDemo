from django.contrib import admin
from .models import Category, Course

admin.site.register(Category)
admin.site.register(Course)

class CourseAdmin(admin.ModelAdmin):
    list_display = ["id","subject","created_date","active"]


# Register your models here.
