# serializers.py

from rest_framework import serializers
from .models import Lesson, LessonView, Product, ProductAccess

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['watched', 'watch_time_seconds']

class ProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAccess
        fields = ['user']

class LessonSerializer(serializers.ModelSerializer):
    lesson_views = LessonViewSerializer(many=True, read_only=True)
    product_accesses = ProductAccessSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['title', 'video_link', 'time', 'lesson_views', 'product_accesses']
