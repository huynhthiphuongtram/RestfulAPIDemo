from rest_framework import viewsets, generics, permissions, parsers
from rest_framework.decorators import action
from rest_framework.views import Response
from .models import Category, Course, Lesson, User
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, LessonDetailSerializer, UserSerializer
from .paginations import CoursePagination


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def filter_queryset(self, queryset):
        q = queryset
        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(subject__icontains=kw)
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            q = q.filter(category_id=cate_id)

        return q

    @action(methods=['get'], detail=True, url_path='lessons')
    def lessons(self, request, pk):
        c = self.get_object()

        lessons = c.lesson_set.filter(active=True)

        kw = self.request.query_params.get('q')
        if kw:
            lessons = lessons.filter(subject__icontains=kw)

        return Response(LessonSerializer(lessons, many=True, context={'request': request}).data)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticated]  # chứng_thực


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'put'], detail=False, url_path='current-user')
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                setattr(u, k, v)
            u.save()

        return Response(UserSerializer(request.user, context={'request': request}).data)