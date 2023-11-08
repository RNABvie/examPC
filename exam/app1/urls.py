from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_, name="login"),
    path("logout/", views.logout_, name="logout"),

    re_path(r'^posts/$', views.post_list, name="posts"),
    re_path(r'^posts/(?P<pk>\d+)/$', views.post_detail, name="post_pk"),
    path('posts/create/', views.post_cr, name="post_cr"),
    path('posts/update/<str:pk>/', views.post_up, name="post_up"),
    path('posts/comment/<str:pk>/', views.comment, name="comment"),

    path('api/users/<str:pk>/', views.UsersList.as_view(), name="user_pk"),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]