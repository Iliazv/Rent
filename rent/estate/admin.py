from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Annoucement, Picture, Favorite, Compilation, Chat, Message

#vitae
admin.site.register(User, UserAdmin)
admin.site.register(Annoucement)
admin.site.register(Picture)
admin.site.register(Favorite)
admin.site.register(Compilation)
admin.site.register(Chat)
admin.site.register(Message)
