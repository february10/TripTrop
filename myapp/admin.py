from django.contrib import admin

# Register your models here.
from .models import Contact, UserProfile, Category, SubCategory, Destination, Feedback, Hotels, Restaurants

admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Destination)
admin.site.register(Feedback)
admin.site.register(Hotels)
admin.site.register(Restaurants)
