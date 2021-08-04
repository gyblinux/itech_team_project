from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Course(models.Model):
    
    course_id = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=50)
    course_description = models.CharField(max_length=128)

    def __str__(self):
        return self.course_id

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0) # new
    likes = models.IntegerField(default=0) # new 
    slug = models.SlugField(unique=True) # chapter6 new

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs) # ??

    class Meta:
        verbose_name_plural = "Categories" # fix last test

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Video(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    username = models.CharField(max_length=12)
    content = models.CharField(max_length=128)
    posttime = models.DateTimeField(default = datetime.now())
    category = models.SlugField()