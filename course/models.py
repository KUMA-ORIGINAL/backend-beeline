from django.db import models


class Course(models.Model):
    name_ru = models.CharField(max_length=200)
    name_kg = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='course/')

    def __str__(self):
        return self.name_ru


class VideoLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name_ru = models.CharField(max_length=200)
    name_kg = models.CharField(max_length=200)
    description_ru = models.TextField(blank=True)
    description_kg = models.TextField(blank=True)
    url_ru = models.URLField(blank=True)
    url_kg = models.URLField(blank=True)

    def __str__(self):
        return self.name_ru


class Test(models.Model):
    LANGUAGES = [
        ("RU", "Русский"),
        ("KG", "Кыргызский"),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGES)
    question = models.CharField(max_length=100)
    answer_true = models.CharField(max_length=100)
    answer_false_1 = models.CharField(max_length=100)
    answer_false_2 = models.CharField(max_length=100)
    answer_false_3 = models.CharField(max_length=100)
    course = models.ManyToManyField(Course)

    def get_courses(self):
        return "/n".join([c.courses for c in self.course.all()])
