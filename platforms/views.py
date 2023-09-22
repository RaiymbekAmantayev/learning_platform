from rest_framework import generics
from .serializers import *
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lesson, ProductAccess, LessonView, Product

class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        products = ProductAccess.objects.filter(user=user).values_list('product', flat=True)
        return Lesson.objects.filter(products__in=products).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
class ProductLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs.get('product_id')
        has_access = ProductAccess.objects.filter(user=user, product_id=product_id).exists()

        if has_access:
            return Lesson.objects.filter(products=product_id)
        else:
            return Lesson.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
class ProductStatsView(APIView):
    def get(self, request):
        products = Product.objects.all()

        stats = []

        for product in products:
            access_count = ProductAccess.objects.filter(product=product).count()
            total_watch_time = LessonView.objects.filter(lesson__products=product).aggregate(total_watch_time=Sum('watch_time_seconds'))['total_watch_time']
            total_students = ProductAccess.objects.filter(product=product).count()
            total_users = User.objects.count()
            purchase_percentage = (access_count / total_users) * 100 if total_users != 0 else 0

            stats.append({
                'product_name': product.name,
                'access_count': access_count,
                'total_watch_time': total_watch_time,
                'total_students': total_students,
                'percent': purchase_percentage,
            })

        return Response(stats)
# Create your views here.
