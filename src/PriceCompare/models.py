# coding: utf8

from django.db import models
from django.contrib.auth.models import User


SITE_CHOICES = (
    ('t', '淘宝'),
    ('a', '亚马逊'),
    ('j', '京东'),
    ('d', '当当'),
)

class Item(models.Model):
    """
    定义单件商品的信息
    """

    name = models.CharField("商品名",max_length=255, default='无名氏')
    price = models.DecimalField("价格", max_digits=10, decimal_places=2, default=0)
    site = models.CharField("来源网站", max_length=1, choices=SITE_CHOICES, default='t')
    url = models.URLField("商品链接", unique=True)
    img = models.URLField("缩略图链接", default='')

    def __unicode__(self):
        return self.name

class UserInfo(models.Model):
    '''
    建立到auth.models.User的一一映射
    记录邮箱地址hash值, 和所有用户-商品之间的多对多关系
    '''
    user = models.OneToOneField(User, primary_key=True, related_name='userinfo')
    hash = models.CharField(max_length=255)

    favorite = models.ManyToManyField(Item, related_name='favorite')

