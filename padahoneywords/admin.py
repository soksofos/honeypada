from django.contrib import admin

# Register your models here.

from .models import Sweetwords
#from models we introduse Swwetwords


admin.site.register(Sweetwords)
#we display them in admin page
