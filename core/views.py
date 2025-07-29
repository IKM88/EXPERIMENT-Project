from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import BlogPost, Event, ContactInquiry, Testimonial
from .forms import ContactForm, TestimonialForm


def home(request):
    """
    Home page view displaying latest blog post, upcoming event, and approved testimonials.
    This is the main landing page for Al-Solution.
    """
    # Get the latest blog post
    latest_post = BlogPost.objects.first()
    
    # Get the next upcoming event
    upcoming_event = Event.objects.filter(event_date__gt=timezone.now()).first()
    
    # Get approved testimonials for the carousel
    approved_testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    
    context = {
        'latest_post': latest_post,
        'upcoming_event': upcoming_event,
        'testimonials': approved_testimonials,
    }
    return render(request, 'core/index.html', context)


def blog_list(request):
    """
    Blog listing page showing all published blog posts.
    Posts are ordered by publication date (newest first).
    """
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'core/blog_list.html', context)


def blog_detail(request, pk):
    """
    Individual blog post detail page.
    Shows the full content of a specific blog post.
    """
    blog_post = get_object_or_404(BlogPost, pk=pk)
    context = {
        'blog_post': blog_post,
    }
    return render(request, 'core/blog_detail.html', context)


def events(request):
    """
    Events listing page displaying all upcoming and past events.
    Events are ordered by date (upcoming first).
    """
    upcoming_events = Event.objects.filter(event_date__gt=timezone.now())
    past_events = Event.objects.filter(event_date__lte=timezone.now())
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'core/events.html', context)


def contact(request):
    """
    Contact page with inquiry form.
    Handles both GET (display form) and POST (process form) requests.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Thank you for your inquiry! We will get back to you within 24 hours.'
            )
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)


def submit_testimonial(request):
    """
    Handle testimonial submission via AJAX from the modal form.
    Testimonials require approval before being displayed publicly.
    """
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Thank you for your testimonial! It will be reviewed and published soon.'
            )
            return redirect('home')
        else:
            messages.error(
                request, 
                'There was an error with your testimonial. Please try again.'
            )
    
    return redirect('home')