from rest_framework import serializers

from lms.models import Course, Lesson, Payment, Subscription
from lms.validators import VideoUrlValidator


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)
    subscribers_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'author', 'price', 'image_preview', 'lessons', 'lessons_count',
                  'subscribers_count', 'is_subscribed',)

    def get_subscribers_count(self, instance):
        return instance.subscription_set.all().count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        try:
            Subscription.objects.get(subscriber=request.user, course=obj)
            return 'Подписан'
        except Subscription.DoesNotExist:
            return 'Не подписан'

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
