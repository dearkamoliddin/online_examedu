from django.contrib import admin
from blog.models import BlogModel, AuthorModel

admin.site.register(BlogModel)
admin.site.register(AuthorModel)

