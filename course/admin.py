
from django.contrib import admin

from course.models import CourseModel, CommentModel, CategoryModel

admin.site.register(CategoryModel)
admin.site.register(CourseModel)
admin.site.register(CommentModel)

