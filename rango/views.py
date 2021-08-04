from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from rango.models import Page, Category, Comment, Course
from rango.forms import PageForm, CategoryForm, VideoForm
from rango.forms import UserForm, UserProfileForm, CommentForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User 
from rango.models import UserProfile


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    
    # Update/set the visits cookie
    request.session['visits'] = visits

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    course_list = Course.objects.all()[:3]
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!', # chapter 3 output
        'categories' : category_list,
        'pages': page_list,
        'courses': course_list
        # 'visits': int(request.COOKIES.get('visits', '1'))
    }
    
    visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']

    response =  render(request, 'rango/index.html', context_dict)
    return response

def about(request):
    # # c10
    # request.session.set_test_cookie()
    # if (request.session.test_cookie_worked()):
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()

    # c10 exercise
    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context_dict)

def forum(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!', # chapter 3 output
        'categories' : category_list,
        'pages': page_list,
        # 'visits': int(request.COOKIES.get('visits', '1'))
    }
    return render(request, 'rango/forum.html', context_dict)

def courses(request):

    courses = Course.objects.all()
    context_dict = {
        'courses': courses,
    }

    return render(request, 'rango/courses.html', context_dict)

def single_course(request, course_id):
    this_course = Course.objects.filter(course_id=course_id)[0]
    topic_list = Category.objects.filter(course=this_course)
    context_dict = {
        'course': this_course,
        'topics': topic_list,
    }
    return render(request, 'rango/course.html', context_dict)

def show_category(request, category_name_slug):
    context_dict= {}
    form = CommentForm()

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    context_dict['form'] = form

    if request.method == 'POST':
        add_comment(request, category_name_slug)
    
    try:
        comment = Comment.objects.filter(category=category_name_slug).order_by('-posttime')[:6]
        context_dict['comments'] = comment
    except Comment.DoesNotExist:
        context_dict['comments'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_comment(request, slug):
    form = CommentForm(request.POST)
    if form.is_valid() and form['content'] != None:
        f = form.save(commit=False)
        f.username = get_server_side_cookie(request, 'username', 'Anonym')
        f.posttime = datetime.now()
        f.category = slug
        f.save()
    else:
        print(form.errors)

@login_required
def add_video(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect(reverse('rango:index'))
    
    form = VideoForm()

    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            if category:
                video = form.save(commit=False)
                video.category = category
                video.views = 0
                video.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_video.html', context=context_dict)


@login_required
def add_category(request):
    ## C9 exercise redirect:
    # if not request.user.is_authenticated:
        # return redirect(reverse('rango:login'))

    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None # for exercise answer: what if the category does not exist handling
    
    # you cannot add a page to a Category that does not exist
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            
                return redirect(reverse('rango:show_category',
                    kwargs={'category_name_slug': category_name_slug}
                ))
        
        else:
            print(form.errors)

    # closing the func
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')





@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
             user_profile = form.save(commit=False) 
             user_profile.user = request.user 
             user_profile.save()
             return redirect(reverse('rango:index')) 
        else:
             print(form.errors) 
    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)


class AboutView(View):
      def get(self, request):
          context_dict = {}
          visitor_cookie_handler(request)
          context_dict['visits'] = request.session['visits']
          return render(request, 'rango/about.html',
                                                 context_dict)



class AddCategoryView(View): 
      @method_decorator(login_required) 
      def get(self, request):
          form = CategoryForm()
          return render(request, 'rango/add_category.html', {'form': form})

      @method_decorator(login_required) 
      def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
           form.save(commit=True)
           return redirect(reverse('rango:index'))
        else: 
            print(form.errors)
        return render(request, 'rango/add_category.html', {'form': form})


class ProfileView(View):
    def get_user_details(self, username):
        try:
           user = User.objects.get(username=username)
        except User.DoesNotExist: 
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture}) 
        return (user, user_profile, form)

    @method_decorator(login_required) 
    def get(self, request, username):
        try:
           (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)

@method_decorator(login_required) 
def post(self, request, username):
    try:
        (user, user_profile, form) = self.get_user_details(username)
    except TypeError:
       return redirect(reverse('rango:index'))
    form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

    if form.is_valid():
         form.save(commit=True)
         return redirect('rango:profile', user.username)
    else: 
        print(form.errors)
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'rango/profile.html', context_dict)

    # return HttpResponse("Since you're logged in, you can see this text!")

# C11 replacement for register, login, logout to auth_app
# def register(request):
#     # A boolean value for telling the template
#     # whether the registration was successful.
#     # Set to False initially. Code changes value to
#     # True when registration succeeds.
#     registered = False

#     # If it's a HTTP POST, we're interested in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
            
#             # Now sort out the UserProfile instance.
#             # Since we need to set the user attribute ourselves,
#             # we set commit=False. This delays saving the model
#             # until we're ready to avoid integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user

#             # Did the user provide a profile picture?
#             # If so, we need to get it from the input form and
#             #put it in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
            
#             # Now we save the UserProfile model instance.
#             profile.save()
            
#             # Update our variable to indicate that the template
#             # registration was successful.
#             registered = True
#         else:
#             # Invalid form or forms - mistakes or something else?
#             # Print problems to the terminal.
#             print(user_form.errors, profile_form.errors)
#     else:
#         # Not a HTTP POST, so we render our form using two ModelForm instances.
#         # These forms will be blank, ready for user input.
#         user_form = UserForm()
#         profile_form = UserProfileForm()
            
#     # Render the template depending on the context.
#     return render(request,
#             'rango/register.html',
#             context = {'user_form': user_form,
#                         'profile_form': profile_form,
#                         'registered': registered
#                     }
#             )

# C11 replacement
# def user_login(request):
#     # If the request is a HTTP POST, try to pull out the relevant information.
#     if request.method == 'POST':
#         # Gather the username and password provided by the user.
#         # This information is obtained from the login form.
#         # We use request.POST.get('<variable>') as opposed
#         # to request.POST['<variable>'], because the
#         # request.POST.get('<variable>') returns None if the
#         # value does not exist, while request.POST['<variable>']
#         # will raise a KeyError exception.
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # Use Django's machinery to attempt to see if the username/password
#         # combination is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)
#         # If we have a User object, the details are correct.
#         # If None (Python's way of representing the absence of a value), no user
#         # with matching credentials was found.
#         if user:
#             # Is the account active? It could have been disabled.
#             if user.is_active:
#                 # If the account is valid and active, we can log the user in.
#                 # We'll send the user back to the homepage.
#                 login(request, user)
#                 request.session['username'] = username
#                 return redirect(reverse('rango:index'))
#             else:
#                 # An inactive account was used - no logging in!
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             # Bad login details were provided. So we can't log the user in.
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#         # This scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object...
#         return render(request, 'rango/login.html')

# # Use the login_required() decorator to ensure only those logged in can
# # access the view.
# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
#     # Take the user back to the homepage.
#     return redirect(reverse('rango:index'))