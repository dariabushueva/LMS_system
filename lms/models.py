from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Course(models.Model):

    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image_preview = models.ImageField(upload_to='media/', **NULLABLE, verbose_name='Превью')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Автор')

    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    update_time = models.DateTimeField(auto_now=True, **NULLABLE, verbose_name='Обновление')

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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):

    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Подписчик')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    status = models.BooleanField(default=True, verbose_name='Статус подписки')

    def __str__(self):
        return f'{self.course} - {self.subscriber}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Payment(models.Model):

    CASH = 'cash'
    TRANSFER = 'transfer'

    METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет')
    ]
    CURRENCY = [
        ('usd', 'USD'),
        ('eur', 'EURO')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    currency = models.CharField(choices=CURRENCY, verbose_name='валюта', default='usd')
    method = models.CharField(max_length=20, verbose_name='Метод оплаты', default='transfer', choices=METHOD_CHOICES)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)

    stripe_id = models.CharField(max_length=100, verbose_name='Stripe ID', **NULLABLE)
    stripe_status = models.CharField(max_length=50, verbose_name='Stripe статус', **NULLABLE)

    def __str__(self):
        return f'{self.user} ({self.course} / {self.lesson})'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
