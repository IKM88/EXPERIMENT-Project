from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Event, ContactInquiry, Testimonial


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for BlogPost model.
    Provides full CRUD capabilities with enhanced list display.
    """
    list_display = ['title', 'publication_date', 'has_image']
    list_filter = ['publication_date']
    search_fields = ['title', 'content']
    readonly_fields = ['publication_date']
    
    def has_image(self, obj):
        """Display whether the blog post has an associated image"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin configuration for Event model.
    Organized by date with upcoming events highlighted.
    """
    list_display = ['title', 'event_date', 'location', 'is_upcoming_display']
    list_filter = ['event_date']
    search_fields = ['title', 'location', 'details']
    ordering = ['event_date']
    
    def is_upcoming_display(self, obj):
        """Display whether the event is upcoming with visual indicator"""
        if obj.is_upcoming:
            return format_html('<span style="color: green;">✓ Upcoming</span>')
        else:
            return format_html('<span style="color: red;">✗ Past</span>')
    is_upcoming_display.short_description = 'Status'


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    """
    Admin configuration for ContactInquiry model.
    Read-only to prevent accidental data alteration with analytics features.
    """
    list_display = ['name', 'email', 'company_name', 'inquiry_type', 'submitted_at']
    list_filter = ['inquiry_type', 'submitted_at']
    search_fields = ['name', 'email', 'company_name', 'message']
    readonly_fields = ['name', 'email', 'company_name', 'inquiry_type', 'message', 'submitted_at']
    ordering = ['-submitted_at']
    
    def has_add_permission(self, request):
        """Disable adding new inquiries through admin"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion for cleanup purposes"""
        return True


def approve_selected_testimonials(modeladmin, request, queryset):
    """
    Custom admin action to approve multiple testimonials at once.
    This allows batch approval of testimonials for efficiency.
    """
    updated = queryset.update(is_approved=True)
    modeladmin.message_user(
        request, 
        f'{updated} testimonial(s) were successfully approved.'
    )
approve_selected_testimonials.short_description = "Approve selected testimonials"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin configuration for Testimonial model.
    Includes approval workflow and batch actions.
    """
    list_display = ['name', 'company', 'rating', 'is_approved', 'submitted_at']
    list_filter = ['is_approved', 'rating', 'submitted_at']
    search_fields = ['name', 'company', 'comment']
    actions = [approve_selected_testimonials]
    ordering = ['-submitted_at']
    
    def get_queryset(self, request):
        """Show all testimonials, with pending ones highlighted"""
        return super().get_queryset(request)


# Customize admin site headers
admin.site.site_header = "Al-Solution Administration"
admin.site.site_title = "Al-Solution Admin"
admin.site.index_title = "Welcome to Al-Solution Administration"