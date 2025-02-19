from django.db import models
from django.forms import JSONField

# Create your models here.


# models per kontaktet

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


# models per videoshow.html


from django.db import models

class Video(models.Model):
#   video_id = models.CharField(max_length=100)
    video_url = models.URLField()  # Ensure this field is in your model
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.title
