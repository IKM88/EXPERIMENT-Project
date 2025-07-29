from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('submit-testimonial/', views.submit_testimonial, name='submit_testimonial'),
]