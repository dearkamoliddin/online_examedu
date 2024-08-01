from django.urls import path
from course.views import CourseView, CourseDetailView

app_name = 'course'

urlpatterns = [
    path('', CourseView.as_view(), name='course'),
    path('course-detail/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),


]
