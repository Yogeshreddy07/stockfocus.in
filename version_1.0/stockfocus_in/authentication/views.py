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
def markets(request):
    return render(request, 'authentication/markets.html')
def news(request):
    return render(request, 'authentication/news.html')
def broker(request):
    return render(request, 'authentication/broker.html')
def learn(request):
    return render(request, 'authentication/learn.html')
def community(request):
    discussions = Discussion.objects.all()
    return render(request, 'authentication/community.html', {'discussions': discussions})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")


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
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
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

def home(request):
    courses = [
        {"title": "Financial Markets", "image": "images/stock1.jpg", "enrolled": 1567},
        {"title": "Trading Basics", "image": "images/stock2.jpg", "enrolled": 1567},
        {"title": "Practical Guide to Trading", "image": "images/stock3.jpg", "enrolled": 2133},
        {"title": "Investment Risk Management", "image": "images/stock4.jpg", "enrolled": 1765},
        {"title": "Stock Market Indices", "image": "images/stock5.jpg", "enrolled": 900},
        {"title": "Stocks and Bonds", "image": "images/stock6.jpg", "enrolled": 1907},
    ]
    return render(request, 'index.html', {'courses': courses})

from django.shortcuts import render

def course_detail(request, course_id):
    return render(request, 'authentication/course_detail.html', {'course_id': course_id})

