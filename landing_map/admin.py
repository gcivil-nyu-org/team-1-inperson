from django.contrib import admin
from .models import Favorite
from .models import Infra_type
from .models import Accessible_location

# Register your models here.

admin.site.register(Infra_type)
admin.site.register(Favorite)
admin.site.register(Accessible_location)
