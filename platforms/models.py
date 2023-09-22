from django.db import models
# models.py
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)    
    def __str__(self):
        return self.name

class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    time = models.IntegerField()
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return self.title

class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watch_time_seconds = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

# Create your models here.
