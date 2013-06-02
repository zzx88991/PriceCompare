# coding: utf8

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
import re
import chardet

# ---
# Custom Fields with Validation rules
# ---

class NameField(models.CharField):
	def to_python(self, value):
		value = value.strip()
		if not re.match(ur'^[a-zA-Z0-9\u4e00-\u9fa5]+$', value):
			raise ValidationError('用户名必须为字母，数字和汉字的组合且不能为空！')
		return value

class PasswordField(models.CharField):
	def to_python(self, value):
		value = value.strip()
		if not re.match(r'^[_a-zA-Z0-9]{6,}$', value):
			raise ValidationError('用户名必须为字母，数字和下划线的组合且至少六位！')
		return value




# ---
# Models
# ---

class User(models.Model):
	name = NameField(max_length = 20, unique=True)
	password = PasswordField(max_length = 15)
	email = models.EmailField(max_length=254, null=True, blank=True)
	
	def __unicode__(self):
		return self.name



class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['name', 'password', 'email']

class Good(models.Model):

	# Enum type for sites
	TAOBAO = 1
	AMAZON = 2
	JINGDONG = 3
	DANGDANG = 4
	SITE_CHOICES = (
			(TAOBAO, 'taobao'),
			(AMAZON, 'amazon'),
			(JINGDONG, 'jingdong'),
			(DANGDANG, 'dangdang'),
		)
	name = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	site = models.IntegerField(choices=SITE_CHOICES)
	picUrl = models.URLField(max_length = 200, null=True, blank=True)

	def __unicode__(self):
		return self.name

