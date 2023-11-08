from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, JsonResponse, HttpResponse
from app1 import models
from django.core.paginator import Paginator
from rest_framework import generics, filters, authentication, permissions, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .filterApi import UserInfoFilter
import re



def post_list(request):
    posts = models.Post.objects.filter(is_active=True)
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(posts, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(request, "app1/post_list.html", context={"current_page": current_page})

@login_required(login_url="login")
def post_detail(request: HttpRequest, pk: str):
    post = models.Post.objects.get(id=pk)
    comments = models.PostComments.objects.filter(post=post)
    return render(request, "app1/post_pk.html", context={"post": post, "comments": comments})

def home(request):
    return render(request, "app1/home.html", context={})

def register(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "app1/register.html")
    elif request.method == "POST":
        # avatar = str(request.POST.get("avatarF", None))
        us_name = str(request.POST.get("usernameF", None)).strip()
        password = str(request.POST.get("passwordF", None)).strip()
        vld_name = re.match(r"[A-Za-z0-9]", us_name)
        vld_pwd = re.match(r"^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!.]).*$", password)
        errorname = ""
        errorpwd = ""
        if vld_pwd is None or vld_name is None:
            if vld_pwd is None:
                errorpwd = "Invalid Password format"
            if vld_name is None:
                errorname = "Invalid Username format"
            generror = "Invalid Format !"
            return render(request, "app1/register.html", context={"error": str(generror), "errorName": str(errorname), "errorPwd": str(errorpwd)})

        try:
            user = User.objects.create(username=us_name, password=make_password(password))
        except Exception as error:
            return render(request, "app1/register.html", context={"error": str(error)})
        return redirect(reverse("login"))
    else:
        raise ValueError("Invalid method")

@login_required
def logout_(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("login"))

def login_(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "app1/login.html")
    elif request.method == "POST":
        us_name = request.POST.get("usernameLog", None)
        password = request.POST.get("passwordLog", None)
        user = authenticate(request, username=us_name, password=password)
        if user is None:
            return render(request, "app1/login.html", {"error": "Invalid data !"})
        login(request, user)
        return redirect(reverse("home"))
    else:
        raise ValueError("Invalid method")

@login_required(login_url="login")
def post_cr(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'app1/post_cr.html')
    elif request.method == "POST":
        try:
            title = str(request.POST['titleF'])
            description = str(request.POST['descrF'])
            image = request.FILES['imageF']
            models.Post.objects.create(author=request.user, title=title, description=description, image=image)
        except Exception as error:
            return render(request, 'app1/post_cr.html', {"error": str(error)})
        return redirect(reverse("posts"))
    else:
        raise ValueError("Invalid method")


@login_required(login_url="login")
def post_up(request: HttpRequest, pk: str) -> HttpResponse:
    post_i = models.Post.objects.get(id=int(pk))

    if request.user != post_i.author:
        return redirect(reverse("posts"))
    elif request.user == post_i.author:
        if request.method == "GET":
            return render(request, "app1/post_up.html", context={"post_i": post_i})
        elif request.method == "POST":
            try:
                post_i.title = str(request.POST.get("updatetitleF")).strip()
                post_i.description = str(request.POST.get("updatedescrF")).strip()
                post_i.image = request.FILES["updateimageF"]
                post_i.save()
                return redirect(reverse("posts"))
            except Exception as error:
                return render(request, 'app1/post_up.html', {"error": str(error)})
        else:
            raise ValueError("Invalid method")
    else:
        return render(request, 'app1/home.html')



@login_required(login_url="login")
def comment(request: HttpRequest, pk: str):
    post = models.Post.objects.get(id=int(pk))
    text = request.POST.get("textCm").strip()
    if text is not "":
        models.PostComments.objects.create(post=post, text=text, author=request.user)

    return redirect(reverse("post_pk", args=(pk,)))



class UsersList(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['is_active',]

    def get(self, request, *args, **kwargs):
        if request.path == '/api/users/get/':
            return self.list(request, *args, **kwargs)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

