from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from stockfocusin import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

from django.shortcuts import render

def community(request):
    return render(request, 'authentication/community.html')  # Make sure 'community.html' exists in templates

def news(request):
    return render(request, 'authentication/news.html')

def learn(request):
    return render(request, 'authentication/learn.html')
def community(request):
    discussions = Discussion.objects.all()
    return render(request, 'authentication/community.html', {'discussions': discussions})

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')  # Safely get 'fname'
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.first_name = fname
        user.save()

        messages.success(request, "Your account has been created successfully!")
        return redirect('signin')

    return render(request, 'authentication/signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or expired.")
            return redirect('signup')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('signup')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname": fname})
        else:
            messages.error(request, "Retry: Username or password incorrect")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Discussion
from .forms import DiscussionForm
from django.contrib import messages

def community(request):
    discussions = Discussion.objects.all()
    return render(request, 'community.html', {'discussions': discussions})

def add_post(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        Discussion.objects.create(title=title, content=content)
        return redirect('community')
    return redirect('community')

def edit_post(request, post_id):
    post = get_object_or_404(Discussion, id=post_id)
    if request.method == "POST":
        form = DiscussionForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community')
    else:
        form = DiscussionForm(instance=post)
    return render(request, 'authentication/edit_post.html', {"post": post})

def delete_post(request, post_id):
    post = get_object_or_404(Discussion, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('community')




from django.shortcuts import render

def course_detail(request, course_id):
    return render(request, 'authentication/course_detail.html', {'course_id': course_id})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Video

@login_required(login_url='/redirect_to_index/')
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        course.enrollment_count += 1
        course.save()
    return redirect('course_detail', course_id=course.id)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    return render(request, 'authentication/course_detail.html', {'course': course, 'videos': videos, 'enrollment': enrollment})

def learn(request):
    courses = Course.objects.all()
    return render(request, 'authentication/learn.html', {'courses': courses})

from django.shortcuts import redirect
from django.contrib import messages

def redirect_to_index(request):
    messages.info(request, 'Please sign in or sign up to access this page.')
    return redirect('home')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Video, UserVideoCompletion

@csrf_exempt
def mark_completed(request, video_id):
    if request.method == 'POST':
        try:
            # Assuming you have a model `Video` and a ManyToManyField `completed_videos` in the `User` model
            video = get_object_or_404(Video, id=video_id)
            user = request.user

            # Add the video to the user's completed videos
            user.profile.completed_videos.add(video)

            # Calculate course completion percentage
            total_videos = video.course.videos.count()
            completed_videos = user.profile.completed_videos.filter(course=video.course).count()
            completion_percentage = (completed_videos / total_videos) * 100

            return JsonResponse({'success': True, 'completion_percentage': completion_percentage})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ollama_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        if not user_input:
            return JsonResponse({"error": "No message provided"}, status=400)

        try:
            # Run Ollama with user input
            process = subprocess.run(
                ["ollama", "run", "deepseek-r1:1.5b"],
                input=user_input,
                text=True,
                capture_output=True,
                check=True
            )
            response = process.stdout.strip()
            return JsonResponse({"response": response})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render
from .models import News  # Assuming you have a News model

def news(request):
    news_list = News.objects.all()  # Fetch all news from the database
    return render(request, 'authentication/news.html', {'news_list': news_list})

