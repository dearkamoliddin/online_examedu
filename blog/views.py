import random
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View
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


class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False
        user.save()
        email = form.cleaned_data['email']
        if send_confirmation_email(email=email):
            return super().form_valid(form)
        else:
            return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:home')
            else:
                form.add_error(None, 'Invalid username or password.')
        return render(request, 'auth/login.html', {'form': form})


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


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('blog:home')


class SendEmailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contact.html')

    def post(self, request, *args, **kwargs):
        subject = request.POST.get("subject")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST.get("email")]
        message = request.POST.get("message")

        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            email = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
            email.send()

        return redirect("blog:home")
