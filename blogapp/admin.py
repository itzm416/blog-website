from django.contrib import admin
from blogapp.models import Category, Post, Profile

# for configration of category admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','token')
    search_fields = ('user',)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag','title','slug','add_date')
    search_fields = ('title',)
class PostAdmin(admin.ModelAdmin):
    list_display = ('image_tag','title','category','slug','add_date')
    search_fields = ('title',)
    list_filter = ('category',)
    list_per_page = 50
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)