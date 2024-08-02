from django.shortcuts import render
from django.views.generic import TemplateView

from course.models import CategoryModel
from teacher.models import TeacherModel


class TeacherView(TemplateView):
    template_name = 'teachers/teacher.html'
    model = TeacherModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = TeacherModel.objects.all()
        context['category'] = CategoryModel.objects.all()
        return context


class TeacherDetailView(TemplateView):
    template_name = 'teachers/teacher-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_id = self.kwargs.get('teacher_id')
        context['teacher'] = TeacherModel.objects.filter(id=teacher_id).first()
        return context
