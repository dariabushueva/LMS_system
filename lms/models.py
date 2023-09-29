from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image_preview = models.ImageField(upload_to='media/', **NULLABLE, verbose_name='Превью')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image_preview = models.ImageField(upload_to='media/', **NULLABLE, verbose_name='Превью')
    video_url = models.URLField(**NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

