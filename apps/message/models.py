#coding=utf-8
from django.db import models
import mongoengine

# Create your models here.
import os,django

#创建数据库的执行命令
# python manage.py makemigrations message
# python manage.py migrate message


class UserMessage(mongoengine.Document):
    name = mongoengine.StringField(max_length=16)
    age = mongoengine.IntField(default=0)


class Blog(mongoengine.Document):
    title = mongoengine.StringField(max_length=100)
    date = mongoengine.StringField(max_length=16)
    classes = mongoengine.StringField(max_length=16)
    tags = mongoengine.StringField(max_length=16)
    zan = mongoengine.StringField(max_length=16)
    comments = mongoengine.StringField(max_length=16)
    img = mongoengine.StringField(max_length=16)
    subtitle = mongoengine.StringField(max_length=16)
    content = mongoengine.StringField(max_length=16)
    url = mongoengine.StringField(max_length=16)
