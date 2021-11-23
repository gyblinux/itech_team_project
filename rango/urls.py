from django.urls import path
from rango import views
from rango.views import AboutView, add_category, show_category

app_name="rango"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('forum/', views.forum, name='forum'),

    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('category/<slug:category_name_slug>/add_video/', views.add_video, name='add_video'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    
    path('add_category/<course_id>', views.add_category, name='add_category'),
    path('add_comment/<slug:category_name_slug>/', views.add_comment, name='add_comment'),
    
    path('courses/', views.courses, name='courses'),
    path('courses/<course_id>/', views.single_course, name='single_course'),
    path('courses/<course_id>/<slug:category_name_slug>/', views.single_category, name='single_category'),
    
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('restricted/', views.restricted, name='restricted'),

    path('search/', views.search, name='search'),

    # lyy test:
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]