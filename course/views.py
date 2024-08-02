from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from course.models import CategoryModel, CourseModel
from django.views.generic import TemplateView


class CourseView(TemplateView):
    template_name = 'courses/course.html'
    model = CourseModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = CourseModel.objects.all()
        context['category'] = CategoryModel.objects.all()
        return context


class CourseDetailView(TemplateView):
    template_name = 'courses/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context['course'] = CourseModel.objects.filter(id=course_id).first()
        return context



