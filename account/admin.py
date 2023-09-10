from django.contrib import admin

from account.models import User, UserProgress, TestResult, UserCourse, VideoLessonProgress, MotivationLetter


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'patronymic', 'location', 'is_verified')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses_completed', 'total_courses', 'number_points')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'points', 'date')


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')


@admin.register(VideoLessonProgress)
class VideoLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user_course', 'video_lesson', 'is_completed', 'time_progress')


@admin.register(MotivationLetter)
class MotivationLetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
