from populate_rango import create_course, populate
from django.http import response
from django.test import TestCase
from django.test import SimpleTestCase
# Create your tests here.

from rango.models import Course, Category
class CourseTest(TestCase):
    def test_add_course_test(self):
        course = create_course("compsci2345", "NLP", "here are some description")
        queried_course = Course.objects.filter(course_id="compsci2345")[0]
        self.assertTrue(course == queried_course)
        