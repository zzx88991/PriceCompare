# coding: utf8

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
import re

# ---
# Custom Fields with Validation rules
# ---

class NameField(models.CharField):

	# A username consists of letters, numbers & Hanzi only
	def to_python(self, value):
		if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fa5]+$', value):
			raise ValidationError('用户名必须为字母，数字和汉字的组合且不能为空！')
		return value





# ---
# Models
# ---

class User(models.Model):
	name = NameField(max_length = 20)
	email = models.EmailField(max_length=254, null=True, blank=True)
	
	def __unicode__(self):
		return self.name



class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['name', 'email']
