from django.urls import path, include, re_path
from rest_framework import routers

from course.views import CourseView, VideoLessonView, TestView

router = routers.DefaultRouter()
router.register(r'course', CourseView, basename='course')
router.register(r'video-lesson', VideoLessonView, basename='video-lesson')
router.register(r'test', TestView, basename='test')

urlpatterns = [
    path('', include(router.urls)),
    re_path('^api/course/video-lesson/(?P<course_id>.+)/$', VideoLessonView.as_view({'get': 'list'}),
            name='course-video-lesson')
]
