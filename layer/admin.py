from django.contrib import admin
from .models import userlog
from django.contrib.auth.models import User

# Create a new user
user = User.objects
# Register your models here.

admin.site.register(userlog)