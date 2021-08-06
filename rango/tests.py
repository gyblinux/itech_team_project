from rango.views import add_category, add_comment
from populate_rango import add_cat, create_course, populate
from django.http import response
from django.test import TestCase
from django.test import SimpleTestCase
# Create your tests here.

from rango.models import Course, Category
from django.urls import reverse
from django.test.client import Client
from django.conf import settings
from rango.forms import CommentForm

class IndexingTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('rango:index'))
        self.assertContains(response, "Learning Hub")

class AuthenticationTest(TestCase):
    def test_auth_component(self):
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)

class CourseTest(TestCase):
    def test_add_course_test(self):
        course = create_course("compsci2345", "NLP", "here are some description")
        queried_course = Course.objects.filter(course_id="compsci2345")[0]
        self.assertTrue(course == queried_course)
        
    def test_courses_view(self):
        course = create_course("compsci3948", "NLP", "here are some descriptions")
        response = self.client.get(reverse('rango:courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "compsci3948")

    def test_single_course_view(self):
        course = create_course("compsci3948", "NLP", "here are some descriptions")
        response = self.client.get(reverse('rango:single_course', kwargs={'course_id': course.course_id}))
        self.assertEqual(response.status_code, 200)

    def test_add_category_to_course(self):
        course = create_course("compsci3948", "NLP", "here are some descriptions")
        add_cat(course, "Test Category", 55, 66)
        response = self.client.get(reverse('rango:single_course', kwargs={'course_id': course.course_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")

class FormTest(TestCase):
    # Valid Form Data
    def test_some_comments(self):
        form = CommentForm(data={'content': "Some test contents"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_empty_comment(self):
        form = CommentForm(data={'content': ""})
        self.assertFalse(form.is_valid())
