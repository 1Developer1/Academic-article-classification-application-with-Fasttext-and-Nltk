from django.contrib import admin
from.models import Users,Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["filename","vector"]  # Detaylı bir şekilde görünmesini sağlar
    # Diğer özel ayarlar...

class User_admin(admin.ModelAdmin):
    list_display=["gender","age","phone"]#bu şekilde yaparak admin panelde detaylı bir şekilde görünmesini sağlayabiliriz.
admin.site.register(Users,User_admin)
admin.site.register(Article, ArticleAdmin)

