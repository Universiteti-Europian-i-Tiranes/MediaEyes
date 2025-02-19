import json
from django.contrib import admin
from .models import Contact

# Register the Contact model
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'country', 'phone', 'subject', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'country')
    list_filter = ('country', 'submitted_at')


from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ( 'video_url', 'title', 'uploaded_at')  # Corrected list_display to use video_url
    search_fields = ('title', 'uploaded_at')  # Correct search fields (ensure no extra spaces)
    list_filter = ('uploaded_at',)  # Uncommented this line to enable filtering by upload date
