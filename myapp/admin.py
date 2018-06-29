from django.contrib import admin
from .models import Comment, Follow, Likes, Posts, Users
# Register your models here.

admin.site.register(Users)
admin.site.register(Posts)
admin.site.register(Follow)
admin.site.register(Likes)
admin.site.register(Comment)
