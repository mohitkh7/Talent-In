from django.contrib import admin
from .models import Year, Branch, Skill, Category
# Register your models here.
admin.site.register(Year)
admin.site.register(Branch)
admin.site.register(Skill)
admin.site.register(Category)