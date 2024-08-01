from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from blog.models import BlogModel
from course.models import CourseModel, CategoryModel
from teacher.models import TeacherModel


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = CourseModel.objects.all()
        context['teacher'] = TeacherModel.objects.all()
        context['category'] = CategoryModel.objects.all()
        context['blog'] = BlogModel.objects.all()
        return context


class HeaderView(TemplateView):
    template_name = 'layouts/header-all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = CategoryModel.objects.all()
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class BlogListView(TemplateView):
    template_name = 'blogs/blog.html'
    model = BlogModel

    def get(self, request, *args, **kwargs):
        blogs = BlogModel.objects.all()
        context = {'blogs': blogs}
        return render(request, 'blogs/blog.html', context)


class BlogDetailView(TemplateView):
    template_name = 'blogs/single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs.get('blog_id')
        context['blog'] = BlogModel.objects.filter(id=blog_id).first()
        return context


def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', context={'message': "Username or password is invalid"})
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', context={"message_user": "Bunday foydalanuvchi allaqachoq mavjud"})

        if password2 == password1:
            new_user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            new_user.set_password(password1)
            new_user.save()
            return redirect('login')
        else:
            return render(request, 'auth/register.html', context={"message_password": "Passwordlar mos kelmadi"})

    return render(request, 'auth/register.html')
