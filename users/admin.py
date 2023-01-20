from django.contrib import admin

# Register your models here.
# from admin_users.models import Admin
# from celebrity.models import Celebrity
# from supporter.models import Supporter
from .models import User

admin.site.register(User)
# admin.site.register(Celebrity)
# admin.site.register(Supporter)
