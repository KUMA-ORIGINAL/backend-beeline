from django.urls import path, include
from rest_framework import routers

from .views import UserRegistrationView, UserVerificationView, UserLoginView, UserLogoutView, MotivationLetterView, \
    TestResultView, UserCourseView, UserProgressView, VideoLessonProgressView

router = routers.DefaultRouter()
router.register(r'user-progress', UserProgressView, basename='user-progress')
router.register(r'user-course', UserCourseView, basename='user-course')
router.register(r'video-lesson-progress', VideoLessonProgressView, basename='video-lesson-progress')
router.register(r'test-result', TestResultView, basename='test-result')
router.register(r'motivation-letter', MotivationLetterView, basename='motivation-letter')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verification/', UserVerificationView.as_view(), name='user-verification'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('', include(router.urls)),
]
