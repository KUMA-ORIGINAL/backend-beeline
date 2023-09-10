from rest_framework import serializers

from .models import User, MotivationLetter, TestResult, UserProgress, VideoLessonProgress, UserCourse


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'is_verified', 'verification_code',
                  'location', 'birth_date',
                  'first_name', 'last_name', 'patronymic']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'


class UserCourseSerializer(serializers.ModelSerializer):
    course_name_ru = serializers.SerializerMethodField()
    course_name_kg = serializers.SerializerMethodField()

    def get_course_name_ru(self, obj):
        return obj.course.name_ru

    def get_course_name_kg(self, obj):
        return obj.course.name_kg

    class Meta:
        model = UserCourse
        fields = '__all__'


class VideoLessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLessonProgress
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    course_name_ru = serializers.SerializerMethodField()
    course_name_kg = serializers.SerializerMethodField()

    def get_course_name_ru(self, obj):
        return obj.course_id.name_ru

    def get_course_name_kg(self, obj):
        return obj.course_id.name_kg

    class Meta:
        model = TestResult
        fields = '__all__'


class MotivationLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationLetter
        fields = '__all__'
