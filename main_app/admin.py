# main_app/admin.py

from django.contrib import admin
from .models import Cat, Feeding, Toy

# registering the models
admin.site.register(Cat)
admin.site.register(Feeding)
admin.site.register(Toy)
