import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    p = Paginator(Post.objects.order_by("-timestamp").all(), 10)
    page = request.GET.get('page', '1')
    posts = p.get_page(page)

    for post in posts:
        post.is_liked_by_user = post.liked_by.filter(username=request.user.username).exists()

    return render(request, "network/index.html", {
        "posts": posts if posts else None
    })


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


@login_required
def create(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    post = Post(author=request.user, text=data.get('text'))
    post.save()

    return JsonResponse({'message': "Post added successfully"}, status=201)


@login_required
def edit(request, post_id):
    if request.method != "PUT":
        return JsonResponse({'error': "PUT request required."}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': "Post does not exist."}, status=400)
    
    if post.author != request.user:
        return JsonResponse({'error': "Forbidden. Unauthorized user"}, status=403)
    
    data = json.loads(request.body)
    post.text = data["text"]
    post.save()

    return HttpResponse(status=204)


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "error": True
        })

    p = Paginator(Post.objects.filter(author=user).order_by("-timestamp"), 10)
    page = request.GET.get('page', '1')
    posts = p.get_page(page)

    for post in posts:
        post.is_liked_by_user = post.liked_by.filter(username=request.user.username).exists()

    return render(request, "network/profile.html", {
        "pr": user,
        "follow": not user.followers.filter(username=request.user.username).exists(),
        "error": False,
        "posts": posts if posts else None
    })


@login_required
def relationship(request, username):
    if request.method != "PUT":
        return JsonResponse({'error': "PUT request required."}, status=400)
    
    if request.user.username == username:
        return JsonResponse({'error': "Forbidden. Can't follow yourself."}, status=403)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': "Invalid username"}, status=400)
    
    if request.user.following.filter(username=username).exists():
        request.user.following.remove(user)
    else:
        request.user.following.add(user)

    request.user.save()
    return HttpResponse(status=204)


@login_required
def like(request, post_id):
    if request.method != "PUT":
        return JsonResponse({'error': "PUT request required."}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': "Post does not exist."}, status=400)
    
    if request.user.likes.filter(pk=post_id).exists():
        request.user.likes.remove(post)
        post.likes_count -= 1
    else:
        request.user.likes.add(post)
        post.likes_count += 1
    
    request.user.save()
    post.save()

    return HttpResponse(status=204)


@login_required
def following(request):
    following_users = request.user.following.all()

    p = Paginator(Post.objects.filter(author__in=following_users).order_by('-timestamp'), 10)
    page = request.GET.get('page', '1')
    posts = p.get_page(page)

    for post in posts:
        post.is_liked_by_user = post.liked_by.filter(username=request.user.username).exists()

    return render(request, "network/following.html", {
        "posts": posts if posts else None
    })
