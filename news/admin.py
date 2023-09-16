from django.contrib import admin
from .models import Author, Category, Post, Comment
from django.contrib.auth.models import Group

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)


admin.site.unregister(Group)
admin.site.register(Group)


authors_group, created = Group.objects.get_or_create(name='authors')

# Register your models here.
