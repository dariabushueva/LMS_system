from django.conf import settings
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


class Payment(models.Model):

    CASH = 'cash'
    TRANSFER = 'transfer'

    METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата оплаты')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(max_length=20, verbose_name='Метод оплаты', default='cash', choices=METHOD_CHOICES)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)

    def __str__(self):
        return f'{self.user} ({self.course} / {self.lesson})'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
