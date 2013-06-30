# coding: utf8

import hashlib

from django import forms
from django.contrib.auth.models import User

from PriceCompare.models import UserInfo


class MyUserCreationForm(forms.Form):
    """
    创建一个用户，信息包括昵称、邮箱地址和密码。
    """

    username = forms.RegexField(label="昵称", max_length=30,
        regex=ur'^[0-9a-zA-Z\u4e00-\u9fa5]+$',
        help_text="必填，只能包含数字、字母和汉字。",
        error_messages={
            'invalid': "昵称只能包含数字、字母和汉字"})

    email = forms.EmailField(label="Email", max_length=254,
                             help_text="必填。用于提供头像和通知服务。")


    password1 = forms.CharField(label="密码",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码",
        widget=forms.PasswordInput,
        help_text="再次输入密码以确认")




    class Meta:
        model = User
        fields = ("username", "email",)

    def clean_username(self):

        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("此昵称已经被注册！")


    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("此邮箱已经被注册！")


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "两次输入的密码不一致！")
        return password2


    def save(self, commit=True):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]

        user = User.objects.create_user(username, email, password)

        if commit:
            user.save()
            user_info = UserInfo(user=user, hash=hashlib.md5(email.lower()).hexdigest())
            user_info.save()
        return user



