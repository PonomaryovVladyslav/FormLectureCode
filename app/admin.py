# Register your models here.
from django.contrib import admin
from .models import Comment, Article, Author

admin.site.register(Comment)
admin.site.register(Article)
admin.site.register(Author)
