from django.db import models
from django.contrib.auth.models import User

class Discussion(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null values for existing data
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, related_name="replies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username}"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    enrollment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Progress in percentage

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class UserVideoCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    completed_videos = models.ManyToManyField(Video, blank=True, related_name='completed_by')

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200)  # Heading of the news
    content = models.TextField()  # Content of the news
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)  # Optional image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the news was created

    def __str__(self):
        return self.title
