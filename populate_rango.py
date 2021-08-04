import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Course, Page

# this function is just a helper function

def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories.
# This might seem a little bit confusing, but it allows us to iterate
# through each data structure, and add the data to our models.
    python_pages = [
        {"title": "Official Python Tutorial", "url": "http://docs.python.org/3/tutorial/", "views": 28},
        {"title": "How to Think like a Computer Scientist", "url": "http://www.greenteapress.com/thinkpython/", "views": 40},
        {"title": "Learn Python in 10 Minutes", "url": "http://www.korokithakis.net/tutorials/python/", "views": 60} 
    ]

    django_pages = [
        {"title": "Official Django Tutorial", "url": "https://docs.djangoproject.com/en/2.1/intro/tutorial01/", "views": 32},
        {"title": "Django Rocks", "url": "http://www.djangorocks.com/", "views": 4},
        {"title": "How to Tango with Django", "url": "http://www.tangowithdjango.com/", "views": 28} 
    ]

    other_pages = [
        {"title": "Bottle", "url": "http://bottlepy.org/docs/dev/", "views": 16},
        {"title": "Flask", "url": "http://flask.pocoo.org", "views": 16} 
    ]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64, "belongs_id": "compsci1234"}, # new 
            "Django": {"pages": django_pages, "views": 64, "likes": 32, "belongs_id": "compsci1234"}, # new
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16, "belongs_id": "compsci5678"}  # new
    }

    course_description = {
        "compsci1234": "Web development is the work involved in developing a Web site for the Internet or an intranet. " \
            "Web development can range from developing a simple single static page of plain text to complex web applications, electronic businesses, and social network services."
        ,  
        "compsci5678": "Machine learning is the study of computer algorithms that improve automatically through experience and by the use of data. " \
            "It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on sample data, known as 'training data', " \
            "in order to make predictions or decisions without being explicitly programmed to do so"
        ,
        "compsci2021": "Web development is the work involved in developing a Web site for the Internet or an intranet. " \
            "Web development can range from developing a simple single static page of plain text to complex web applications, electronic businesses, and social network services."
        ,
        "compsci2333": "A package manager or package-management system is a collection of software tools that automates the process of installing, upgrading, " \
            "configuring, and removing computer programs for a computer's operating system in a consistent manner. A package manager deals with packages, distributions of software and data in archive files."
    }

    courses = {
        "compsci1234": {"id": "compsci1234", "name": "Web Development", "description": course_description["compsci1234"]},
        "compsci5678": {"id": "compsci5678", "name": "Machine Learning", "description": course_description["compsci5678"]},
        "compsci2021": {"id": "compsci2021", "name": "Web Application Development", "description": course_description["compsci1234"]},
        "compsci2333": {"id": "compsci2333", "name": "Package Manager", "description": course_description["compsci2333"]},
    }
    # If you want to add more catergories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.
    for course_id, course_value in courses.items():
        create_course(course_id, course_value["name"], course_value["description"])

    for cat, cat_data in cats.items():
        c = add_cat(Course.objects.filter(course_id=cat_data["belongs_id"])[0] , cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p
    
def add_cat(course, name, views, likes):
    c = Category.objects.get_or_create(course=course, name=name)[0]
    
    # added:
    c.views = views
    c.likes = likes
    
    c.save()
    return c

def create_course(a_course_id, a_course_name, a_course_description):
    new_course = Course.objects.get_or_create(course_id=a_course_id, \
        course_name=a_course_name, course_description=a_course_description)[0]
    new_course.save()
    return new_course

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()