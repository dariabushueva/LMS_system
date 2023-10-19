from django.shortcuts import redirect
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Course, Lesson, Payment, Subscription
from lms.pagination import LMSPagination
from lms.permissions import IsModeratorOrIsAuthor, IsAuthor, IsSubscriber
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from lms.services import create_stripe_checkout_session, get_stripe_payment
from lms.tasks import send_updated_email


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for Course """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LMSPagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.author = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]

        elif self.action == 'destroy':
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsModeratorOrIsAuthor]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """ Lesson create endpoint """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.author = self.request.user
        new_course.save()

        send_updated_email.delay(new_course.course_id)


class LessonListAPIView(generics.ListAPIView):
    """ Lesson list endpoint """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LMSPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Lesson detail endpoint """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModeratorOrIsAuthor]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Lesson update endpoint """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModeratorOrIsAuthor]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Lesson delete endpoint """

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthor]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ ViewSet for subscription """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        new_subs = serializer.save()
        new_subs.subscriber = self.request.user
        new_subs.save()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSubscriber]
        return [permission() for permission in permission_classes]


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Payment create endpoint """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        course_id = request.data.get('course')
        course = Course.objects.get(pk=course_id)
        session = create_stripe_checkout_session(course_id)

        Payment.objects.create(
            user=self.request.user,
            amount=session["amount_total"],
            course=course,
            stripe_id=session['id'],
            stripe_status=session['status']
        )
        return redirect(session.url)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Payment retrieve endpoint """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payment_detail = get_stripe_payment(pk=kwargs.get('pk'))
        return Response(status=status.HTTP_200_OK, data=payment_detail)


class PaymentListAPIView(generics.ListAPIView):
    """ Payment list endpoint """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]




