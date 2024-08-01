from django.contrib import admin
from blog.models import BlogModel, AuthorModel, UserConfirmationModel

admin.site.register(BlogModel)
admin.site.register(AuthorModel)
admin.site.register(UserConfirmationModel)


