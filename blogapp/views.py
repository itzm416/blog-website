from django.conf import settings
from django.shortcuts import redirect,render
from blogapp.models import Category, Post, Profile
from django.contrib.auth import authenticate,login, logout, update_session_auth_hash
from blogapp.forms import SignUpForm, LoginForm, AddPostForm, UserPasswordChange, UserPasswordReset
from django.contrib import messages
from random import sample

import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User

from django.urls import reverse
from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'index.html')

def home(request):
    
    staff = User.objects.filter(is_staff=True)

    # create list of user id
    staff_id = [user.id for user in staff]

    # for random posts
    staff_post = list(Post.objects.filter(author__in=staff_id))
    l = (len(staff_post))
    s_post = sample(staff_post, l)

    # for recent post
    recent_post = list(Post.objects.filter(author__in=staff_id).order_by('-add_date'))
    recent = recent_post[0:8]

    cats = Category.objects.all()
    data = {
        'post':s_post,
        'recentpost':recent,
        'cats':cats,
        'h':'active'
    }
    
    return render(request, 'home.html', data)

def blog(request):
    # for create by super user or random user
    p = list(Post.objects.all())
    l = len(p)
    post = sample(p, l)

    # for recent post created by super user or random user
    recent_post = list(Post.objects.all().order_by('-add_date'))
    recent = recent_post[0:8]

    cats = Category.objects.all()
    data = {
        'post':post,
        'recentpost':recent,
        'cats':cats,
        'b':'active'
    }
    return render(request, 'blog.html', data)

def admin_delete_home(request, id):
    id = Post.objects.get(pk=id)
    id.delete()
    messages.success(request,'Post Deleted Successfully !')
    return redirect('home')

def admin_delete_blog(request, id):
    id = Post.objects.get(pk=id)
    id.delete()
    messages.success(request,'Post Deleted Successfully !')
    return redirect('blog')

def admin_update_post(request,slug):
    if request.user.is_authenticated:
        cats = Category.objects.all()
        if request.method=='POST':
            id = Post.objects.get(slug=slug)
            fm = AddPostForm(request.POST,request.FILES,instance=id)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Post Updated Successfully !')
                return HttpResponseRedirect(reverse('post', args=[str(slug)]))
            else:
                return render(request, 'updatepost.html',{'form':fm, 'cats':cats})
        else:       
            id = Post.objects.get(slug=slug)
            fm = AddPostForm(instance=id)
            return render(request, 'updatepost.html',{'form':fm, 'cats':cats})
    else:
        return redirect('home')

def about(request):
    cats = Category.objects.all()
    data = {
        'cats':cats,
        'ab':'active'
    }
    return render(request, 'about.html', data)

def post(request, slug):
    post = Post.objects.get(slug=slug)

    postviews = Post.objects.get(slug=slug)
    postviews.blogviews = postviews.blogviews+1
    views = postviews.save()

    cats = Category.objects.all()
    data = {
        'post':post,
        'cats':cats,
        'view':views
    }
    return render(request, 'post.html', data)

def category(request, slug):
    cats = Category.objects.all()
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category)
    data = {
        'cats':cats,
        'posts':posts,
        'category':category,
        'c':'active'
    }
    return render(request, 'category.html', data)

def add_post(request):
    if request.user.is_authenticated:
        cats = Category.objects.all()
        if request.method == 'POST':
            fm = AddPostForm(request.POST,request.FILES)
            if fm.is_valid():
                form = fm.save(commit=False)
                form.author = request.user
                form.save()
                messages.success(request,'Post Added Successfully !')
                return redirect('dashboard')
            return render(request, 'addpost.html', {'form':fm, 'cats':cats})
        else:
            fm = AddPostForm()
            return render(request, 'addpost.html', {'form':fm, 'cats':cats})
    else:
        return redirect('home')

def search_post(request):
    cats = Category.objects.all()
    query = request.GET['query']
    posts = Post.objects.filter(title__icontains=query)
    return render(request,'search.html',{'posts':posts, 'cats':cats})

def update_post(request,id):
    if request.user.is_authenticated:
        cats = Category.objects.all()
        if request.method=='POST':
            id = Post.objects.get(pk=id)
            fm = AddPostForm(request.POST,request.FILES,instance=id)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Post Updated Successfully !')
                return redirect('dashboard')
            else:
                return render(request, 'updatepost.html',{'form':fm, 'cats':cats})
        else:       
            id = Post.objects.get(pk=id)
            fm = AddPostForm(instance=id)
            return render(request, 'updatepost.html',{'form':fm, 'cats':cats})
    else:
        return redirect('home')

def delete_post(request,id):
    id = Post.objects.get(pk=id)
    id.delete()
    messages.success(request,'Post Deleted Successfully !')
    return redirect('dashboard')

def user_dashboard(request):
    if request.user.is_authenticated:
        cats = Category.objects.all()
        posts = Post.objects.filter(author=request.user)
        return render(request, 'dashboard.html',  {'cats':cats, 'post':posts, 'd':'active'})
    else:
        return redirect('home')

def user_login(request):
    if not request.user.is_authenticated:
        cats = Category.objects.all()
        if request.method=='POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upassword = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upassword)
                login(request, user)
                messages.success(request,'User Login Successfully !')
                return redirect('home')
            else:
                return render(request, 'login.html', {'form':fm, 'cats':cats})
        else:
            fm = LoginForm()
            return render(request, 'login.html', {'form':fm, 'cats':cats})
    else:
        return redirect('home')

def user_logout(request):
    logout(request)
    messages.success(request,'User Logout Successfully !')
    return redirect('home')

# ---------------------------------Signup---------------------------------------------

def email_verification(host ,email, token):
    subject = "Verify Email"
    message = f"Hi check your link http://{host}/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_account_verify(request, token):
    pro_obj = Profile.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)

    if user.is_active == False:
        user.is_active = True
        user.save()
        return render(request, 'email-verification/send_email_verified.html')
    else:
        return render(request, 'email-verification/send_email_already_verified.html')

def user_signup(request):  
    if not request.user.is_authenticated:
        cats = Category.objects.all()
        if request.method == 'POST':  
            form = SignUpForm(request.POST)  
            if form.is_valid():  
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  

                uid = uuid.uuid4()
                
                pro_obj = Profile(user=user, token=uid)
                pro_obj.save()
                
                host = request.get_host()
                email_verification(host, user.email, uid)

                return render(request, 'email-verification/send_email_done.html')
            else:
                return render(request, 'signup.html', {'form': form, 'cats':cats}) 
        else:  
            form = SignUpForm()  
            return render(request, 'signup.html', {'form': form, 'cats':cats}) 
    else:
        return redirect('home')

# ----------------------------passwordreset-------------------------------------

def email_password_reset(host, email, token):
    subject = "Password Reset Link"
    message = f"Hi check your link http://{host}/password-reset/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_password_change(request):
    if request.user.is_authenticated:
        cats = Category.objects.all()
        if request.method == 'POST':  
            form = UserPasswordChange(user=request.user, data=request.POST) 
            if form.is_valid():  
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request,'Password changed Successfully !')
                return redirect('dashboard')
            else:
                return render(request, 'password-change/change_password.html', {'form': form, 'cats':cats})
        else:
            form = UserPasswordChange(user=request.user) 
            return render(request, 'password-change/change_password.html', {'form': form, 'cats':cats})
    else:
        return redirect('home')

def user_email_send(request):
    if request.method == 'POST':  
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            pro_obj = Profile.objects.get(user=user)
            host = request.get_host()
            email_password_reset(host, email, pro_obj.token)
        except (User.DoesNotExist,Profile.DoesNotExist) as e:
            messages.warning(request,'Invalid Email !')
            return render(request, 'password-change/password_reset_email.html')

        return render(request, 'password-change/password_reset_email_done.html')
    else:
        return render(request, 'password-change/password_reset_email.html')

def user_password_reset(request, token):
    pro_obj = Profile.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)
    cats = Category.objects.all()
    if request.method == 'POST':  
        form = UserPasswordReset(user=user, data=request.POST) 
        if form.is_valid():  
            form.save()
            return render(request, 'password-change/password_reset_done.html')
        else:
            return render(request, 'password-change/password_reset.html', {'form': form, 'cats':cats})
    else:
        form = UserPasswordReset(user=user) 
        return render(request, 'password-change/password_reset.html', {'form': form, 'cats':cats})
 
