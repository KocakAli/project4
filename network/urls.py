
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submit",views.submit, name="submit"),
    path("profile/<str:name>",views.profile,name="profile"),
    path("following",views.fw,name="following"),
    

    #API
    path('post/<int:num>',views.get_posts,name='get_posts'),
    path('like',views.like_post,name='like_post'),
    path('edit',views.edit,name='edit_post'),
    path('p/<str:name>/<int:num>',views.p,name='p'),
    path('fw_posts/<int:num>',views.fw_posts,name='fw_posts'),
    path('pf/<str:name>',views.pf,name='pf'),
    path('follow',views.follow,name='follow'),
]
