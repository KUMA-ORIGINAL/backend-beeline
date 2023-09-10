from django.db.models import Count
from rest_framework import viewsets

from .models import Course, VideoLesson, Test
from course.serializers import CourseSerializer, VideoLessonSerializer, TestSerializer
from course.permissons import ReadOnlyOrAdminPermission


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(videos_count=Count('videolesson'))
    serializer_class = CourseSerializer
    permission_classes = [ReadOnlyOrAdminPermission]


class VideoLessonView(viewsets.ModelViewSet):
    serializer_class = VideoLessonSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_queryset(self):
        queryset = VideoLesson.objects.all()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = VideoLesson.objects.filter(course_id=course_id)
        return queryset



class TestView(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_queryset(self):
        queryset = Test.objects.all()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = Test.objects.filter(course_id=course_id)
        return queryset


#
# class DirectionApiView(APIView):
#     def get(self, request):
#         d = Direction.objects.all()
#         for i in d:
#             i.objects.annotate(count_video=VideoLesson.objects.count(direction=i.id))
#         # return Response({'directions': })
#
#     def post(self, request):
#         serializer = DirectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'direction': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method PUT not allowed'})
#
#         try:
#             instance = Direction.objects.get(pk=pk)
#         except Direction.DoesNotExist:
#             return Response({'error': 'Method PUT not allowed'})
#
#         serializer = DirectionSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'direction': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method DELETE not allowed'})
#
#         d = Direction.objects.get(pk=pk).delete()
#         return Response({'direction': d})
#
