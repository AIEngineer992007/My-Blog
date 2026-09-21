from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='like_posts', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='dislike_posts', blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts-detail", kwargs={"pk": self.pk})

class ContactMessage(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_sent']
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_posted']
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"