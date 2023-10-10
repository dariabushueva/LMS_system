from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            author=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Test_lesson',
            course=self.course,
        )

    def test_create_lesson(self):

        data = {
            'title': self.lesson.title,
            'course': self.course.id,
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': (self.lesson.id + 1), 'title': self.lesson.title, 'description': None, 'image_preview': None, 'video_url': None,
             'course': self.course.id, 'author': self.user.id}
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):

        response = self.client.get(
            '/lesson/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['results'],
            [{'id': self.lesson.id, 'title': self.lesson.title, 'description': None, 'image_preview': None, 'video_url': None,
              'course': self.course.id, 'author': None}]
        )

    def test_retrieve_lesson(self):

        response = self.client.get(
            f'/lesson/{self.lesson.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'title': 'Test_lesson', 'description': None, 'image_preview': None, 'video_url': None,
             'course': self.course.id, 'author': None}
        )

    def test_update_lesson(self):

        data = {
            'title': 'Test_updated_lesson',
        }
        response = self.client.patch(
            f'/lesson/update/{self.lesson.id}/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'title': 'Test_updated_lesson', 'description': None, 'image_preview': None,
             'video_url': None, 'course': self.course.id, 'author': None}
        )

    def test_destroy_lesson(self):

        response = self.client.delete(
            f'/lesson/destroy/{self.lesson.id}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Subscription.objects.all().delete()


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            author=self.user
        )
        self.subs = Subscription.objects.create(
            course=self.course,
        )

    def test_create_subscription(self):
        data = {
            'course': self.course.id,
        }
        response = self.client.post(
            '/subscription/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': (self.subs.id + 1), 'subscriber': self.user.id, 'course': self.course.id}
        )
        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_destroy_subscription(self):

        response = self.client.delete(
            f'/subscription/{self.subs.id}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Subscription.objects.all().delete()

