from django.contrib import admin
from .models import PostModel
from django.contrib.auth.models import  Group


class PostModelPanel (admin.ModelAdmin) : 
    list_display = ['user','title','created_at']
    search_fields = ['title']
    ordering = ['-created_at']



admin.site.register(PostModel, PostModelPanel)



admin.site.unregister(Group)