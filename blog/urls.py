from django.urls import path

from blog.views import HomePageView, AboutView, ContactView, BlogListView, BlogDetailView, LoginView, RegisterView, \
    SendEmailView, confirmation_view, LogoutView

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    #path('category/', HeaderView.as_view(), name='category'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog_list/', BlogListView.as_view(), name='blog-list'),
    path('blog_detail/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send_email/', SendEmailView.as_view(), name='send_email'),
    path('confirm/', confirmation_view, name='confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),


]
