from datetime import date

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

from course.models import Course, VideoLesson


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    birth_date = models.DateField(default=date.today)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} | {self.first_name} | {self.last_name}'


class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses_completed = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)
    number_points = models.PositiveIntegerField(default=0)


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now=True)


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} | {self.course}'


class VideoLessonProgress(models.Model):
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE)
    video_lesson = models.ForeignKey(VideoLesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    time_progress = models.DurationField()


class MotivationLetter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    points = models.PositiveIntegerField(default=0, blank=True,
                                         validators=[MaxValueValidator(10)])

