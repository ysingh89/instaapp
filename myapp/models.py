from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=256, primary_key=True)
    password = models.CharField(max_length=128)
    userimage = models.FileField(null=True,blank=True)
    fname = models.CharField(max_length=256)
    lname = models.CharField(max_length=256)
    phone = models.BigIntegerField()
    email = models.EmailField(blank=True,null=True)

class Posts(models.Model):
    title = models.CharField(max_length=512)
    image = models.FileField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey('Users',on_delete=models.CASCADE)

class Likes(models.Model):
    postid = models.ForeignKey('Posts',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey('Users',on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.ForeignKey('Users', on_delete=models.CASCADE)
    following = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='following_this_person')

class Comment(models.Model):
    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey('Users', on_delete=models.CASCADE)
    postid = models.ForeignKey('Posts', on_delete=models.CASCADE)
