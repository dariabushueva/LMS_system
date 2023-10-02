from rest_framework import serializers

from lms.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'image_preview', 'lessons', 'lessons_count')

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
