from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from  .models import Following, Posts,Followers
from datetime import datetime
from .models import User,Like
import math
from django.core.paginator import Paginator
from itertools import chain


def index(request):
    return render(request, "network/index.html")

    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='/login')
def profile(request, name):
    user = User.objects.get(username=name)
    cur_user = request.user.username
    
    return render(request,"network/profile.html",{
        'name':user.username,
        'user':cur_user
    })

@login_required(login_url='/login')
@csrf_exempt
def submit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    text = data.get("text")
    user = request.user
    now = datetime.now()
    time = now.strftime("%d %B %Y, %H:%M:%S")
    post = Posts(p_text=text, p_user=user,p_username = user.username,p_time = time)
    post.save()
    
    
    

    return HttpResponseRedirect(reverse("index"))

def get_posts(request,num):
    print(num)
    user = request.user
    username = user.username
    ordered_p = Posts.objects.order_by('-p_time')
    post_json = list(ordered_p.values())
    print(post_json)
    max_page= math.ceil(len(post_json)/10)
    
    page_num = 10
    print(page_num)
    p = Paginator(post_json,page_num)
    page = p.page(num)

    jsonData ={
        'posts' : page.object_list,
        'username' : username,
        'maxPage':max_page
    }
    
    return JsonResponse(jsonData,safe=False)

@login_required(login_url='/login')
@csrf_exempt
def like_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    id = data.get("post_id")
    user = request.user
    post = Posts.objects.get(pk = id)

    check = Like.objects.filter(l_users =user, l_post = post)
    print(len(check))
    if len(check) !=0:
        post.p_like -=1
        check.delete()
    else:
        post.p_like +=1
        like = Like(l_users =user, l_post = post)
        like.save()

    post.save()
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
@csrf_exempt
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    id =data.get("id")
    text =data.get("post")
    print(id)

    print(text)
    post = Posts.objects.get(pk = id)
    post.p_text = text
    post.save()

    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def fw(request):
    return render(request,'network/following.html')

@login_required(login_url='/login')
def fw_posts(request,num):
    user = request.user
    username = user.username
    fg = Followers.objects.filter(follower=user)
    a = list(fg.values())

    users = []
    for user in a:
        users.append(user['fs_user_id'])
    

    users_query=[]
    for query in users:
        a_user = Posts.objects.filter(p_user=query).order_by('-p_time')
        users_query.append(list(a_user.values()))
    
    
    posts = list(chain(*users_query))
    max_page= math.ceil(len(posts)/10)
    
    page_num = 10
    print(page_num)
    p = Paginator(posts,page_num)
    page = p.page(num)
    response_data = {
        'posts' : page.object_list,
        'maxPage':max_page,
        'username' : username,
    }
    
    return JsonResponse(response_data,safe=False)


@login_required(login_url='/login')
def p(request,name,num):
    user = User.objects.get(username=name)
    cur_user = request.user
    cur_user_uname = cur_user.username
    posts = Posts.objects.filter(p_user = user).order_by('-p_time')
    posts_list = list(posts.values())
    max_page= math.ceil(len(posts_list)/10)
    page_num = 10
    print(page_num)
    p = Paginator(posts_list,page_num)
    page = p.page(num)

    jsonData ={
        'posts': page.object_list,
        'username':cur_user_uname,
        'maxPage':max_page
    }


    return JsonResponse(jsonData,safe=False)

@login_required(login_url='/login')
def pf(request,name):
    user = User.objects.get(username=name)
    followers = Followers.objects.filter(fs_user = user.id)
    following = Followers.objects.filter(follower = user.id)
    fs_len = len(followers)
    fg_len = len(following)
    jsonData ={
        'fs' : fs_len,
        'fg' : fg_len,
    }
    return JsonResponse(jsonData,safe=False)

@login_required(login_url='/login')
@csrf_exempt
def follow(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    username = User.objects.get(pk=request.user.id)
    followed = User.objects.get(username = data.get("name"))

    check = Followers.objects.filter(follower =username, fs_user = followed)
    print(len(check))
    if len(check) !=0:
            check.delete()
    else:
        follow = Followers(follower = username,fs_user = followed)
        follow.save()


    
    
    return JsonResponse({"follow": "Successful"})

