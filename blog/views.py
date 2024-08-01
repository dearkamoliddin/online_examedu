import random

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from conf.settings import EMAIL_HOST_USER
from blog.forms import RegistrationForm, LoginForm
from blog.models import BlogModel, UserConfirmationModel
from course.models import CourseModel, CategoryModel
from teacher.models import TeacherModel
from django.core.mail import EmailMessage, get_connection, send_mail


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


def send_confirmation_email(email):
    subject = 'Confirm Your Email'
    code = random.randint(1000, 9999)
    if UserConfirmationModel.objects.filter(code=code).exists():
        send_confirmation_email(email)
    emails = [email]
    from_email = EMAIL_HOST_USER
    if send_mail(subject=subject, message=str(code), from_email=from_email, recipient_list=emails):
        UserConfirmationModel.objects.create(
            code=code,
            email=email,
            is_active=True,
        )
        return True
    else:
        return False


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            if send_confirmation_email(email=form.cleaned_data['email']):
                return render(request, 'auth/confirmation.html')
            else:
                return redirect('blog:home')
        else:
            return HttpResponse(form.errors)
    else:
        return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:home')
            else:
                return render(request, 'auth/login.html')
        else:
            return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')


def confirmation_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_code = UserConfirmationModel.objects.get(code=code)
        if user_code:
            user = User.objects.get(email=user_code.email)
            user.is_active = True
            user.save()
            return redirect('blog:login')
        else:
            return redirect('blog:home')
    else:
        return render(request, 'auth/confirmation.html')

# def register_view(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password']
#         password2 = request.POST['password2']
#         if User.objects.filter(username=username).exists():
#             return render(request, 'auth/register.html', context={"message_user": "Bunday foydalanuvchi allaqachoq mavjud"})
#
#         if password2 == password1:
#             new_user = User(first_name=first_name, last_name=last_name, username=username, email=email)
#             new_user.set_password(password1)
#             new_user.save()
#             return redirect('login')
#         else:
#             return render(request, 'auth/register.html', context={"message_password": "Passwordlar mos kelmadi"})
#
#     return render(request, 'auth/register.html')


def send_email(request):
    if request.method == "POST":
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            subject = request.POST.get("subject")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email"), ]
            message = request.POST.get("message")
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
        return redirect("blog:home")

    return render(request, 'contact.html')
