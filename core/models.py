from django.db import models
from django.urls import reverse
from django.utils import timezone


class BlogPost(models.Model):
    """
    Model for blog posts on the Al-Solution website.
    Allows for dynamic content management through the admin panel.
    """
    title = models.CharField(max_length=200, help_text="The title of the blog post")
    content = models.TextField(help_text="The main content of the blog post")
    publication_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='blog_images/', 
        blank=True, 
        null=True,
        help_text="Optional image for the blog post"
    )
    
    class Meta:
        ordering = ['-publication_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})


class Event(models.Model):
    """
    Model for events and webinars hosted by Al-Solution.
    Displays upcoming events on the website.
    """
    title = models.CharField(max_length=200, help_text="The name of the event")
    event_date = models.DateTimeField(help_text="Date and time when the event will occur")
    location = models.CharField(
        max_length=300, 
        help_text="Event location (can be virtual link or physical address)"
    )
    details = models.TextField(help_text="Detailed description of the event")
    image = models.ImageField(
        upload_to='event_images/', 
        blank=True, 
        null=True,
        help_text="Optional promotional image for the event"
    )
    
    class Meta:
        ordering = ['event_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"
    
    @property
    def is_upcoming(self):
        """Check if the event is in the future"""
        return self.event_date > timezone.now()


class ContactInquiry(models.Model):
    """
    Model to store contact form submissions from potential clients.
    Provides analytics and lead management through the admin panel.
    """
    INQUIRY_CHOICES = [
        ('general', 'General Question'),
        ('demo', 'Request a Demo'),
        ('prototyping', 'Prototyping Service Inquiry'),
        ('consulting', 'AI Consulting'),
        ('partnership', 'Partnership Opportunity'),
        ('support', 'Technical Support'),
    ]
    
    name = models.CharField(max_length=100, help_text="Contact person's full name")
    email = models.EmailField(help_text="Contact person's email address")
    company_name = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Name of the company (optional)"
    )
    inquiry_type = models.CharField(
        max_length=20, 
        choices=INQUIRY_CHOICES,
        help_text="Type of inquiry for better categorization"
    )
    message = models.TextField(help_text="Detailed message from the contact")
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
    
    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"


class Testimonial(models.Model):
    """
    Model for client testimonials and reviews.
    Includes approval system to moderate content before display.
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    name = models.CharField(max_length=100, help_text="Name of the person providing testimonial")
    company = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Company name (optional)"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        help_text="Star rating from 1 to 5"
    )
    comment = models.TextField(help_text="Testimonial comment")
    is_approved = models.BooleanField(
        default=False,
        help_text="Whether this testimonial is approved for public display"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"
    
    @property
    def star_range(self):
        """Returns a range for template iteration to display stars"""
        return range(self.rating)