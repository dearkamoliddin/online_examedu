from django.shortcuts import render
from django.views.generic import TemplateView

from teacher.models import TeacherModel


class TeacherView(TemplateView):
    template_name = 'teachers/teacher.html'
    model = TeacherModel

    def get(self, request, *args, **kwargs):
        teachers = TeacherModel.objects.all()
        context = {'teachers': teachers}
        return render(request, 'teachers/teacher.html', context)


class TeacherDetailView(TemplateView):
    template_name = 'teachers/teacher-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_id = self.kwargs.get('teacher_id')
        context['teacher'] = TeacherModel.objects.filter(id=teacher_id).first()
        return context
