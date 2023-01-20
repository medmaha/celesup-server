from django.contrib import admin
from .models import Post
from .picture_model import Photo

# Register your models here.


admin.site.register(Photo)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'caption', 'key']
    # prepopulated_fields = {'slug': ('name',)}

