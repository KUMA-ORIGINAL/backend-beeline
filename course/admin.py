from django.contrib import admin

from course.models import Course, VideoLesson, Test


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_kg')


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name_ru', 'name_kg')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('get_courses', 'language', 'question')

    def get_courses(self, obj):
        return "/n".join([c.courses for c in obj.course.all()])
