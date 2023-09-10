from rest_framework import serializers

from course.models import Course, VideoLesson, Test


class CourseSerializer(serializers.ModelSerializer):
    videos_count = serializers.SerializerMethodField()

    def get_videos_count(self, obj):
        return obj.videolesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
