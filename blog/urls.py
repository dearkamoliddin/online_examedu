from django.urls import path

from blog.views import HomePageView, AboutView, ContactView, BlogListView, BlogDetailView, login_view, register_view, \
    send_email, confirmation_view

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    #path('category/', HeaderView.as_view(), name='category'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog_list/', BlogListView.as_view(), name='blog-list'),
    path('blog_detail/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('send_email/', send_email, name='send_email'),
    path('confirm/', confirmation_view, name='confirm'),


]
