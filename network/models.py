from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey



class User(AbstractUser):
    pass

class Posts(models.Model):
    p_text = models.CharField(max_length=256)
    p_user = ForeignKey(User, on_delete=models.CASCADE, related_name='users_p')
    p_username = models.CharField(max_length=16)
    p_like = models.IntegerField(default=0)
    p_time = models.CharField(max_length=64)


class Like(models.Model):
    l_users = ForeignKey(User, on_delete=CASCADE,related_name="users_l")
    l_post = ForeignKey(Posts, on_delete=CASCADE,related_name="post_l")

class Followers(models.Model):
    fs_user = ForeignKey(User, on_delete=CASCADE,related_name="users_fs")
    follower = ForeignKey(User, on_delete=CASCADE,related_name="users_follower")

class Following(models.Model):
    fg_user = ForeignKey(User, on_delete=CASCADE,related_name="users_fg")
    following = ForeignKey(User, on_delete=CASCADE,related_name="users_following")

