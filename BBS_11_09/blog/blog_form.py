from django import forms
from django.forms import widgets
from django.forms import ValidationError
from . import models
from django.contrib import auth


class Register(forms.Form):
    username = forms.CharField(required=True,
                               label='用户名'
                               ,
                               error_messages={'required': '不能为空'}
                               ,
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(required=True,
                               label='密码',
                               error_messages={'required': '不能为空'}
                               ,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )
    re_password = forms.CharField(required=True,
                                  label='确认密码',
                                  error_messages={'required': '不能为空'},
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                  )

    def clean_username(self):
        print(self.cleaned_data)
        username = self.cleaned_data.get('username')
        if models.User.objects.filter(username=username):
            raise ValidationError('用户名已经存在')
        else:
            return username

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')


class Login(forms.Form):

    username = forms.CharField(required=True,
                               label='用户名'
                               ,
                               error_messages={'required': '不能为空'}
                               ,
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(required=True,
                               label='密码',
                               error_messages={'required': '不能为空'}
                               ,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )

    def clean_username(self):
        print(self.cleaned_data)
        username = self.cleaned_data.get('username')
        if not models.User.objects.filter(username=username):
            raise ValidationError('用户名不存在')
        else:
            return username

    # def clean(self):
    #     password = self.cleaned_data.get('password')
    #     username = self.cleaned_data.get('username')
    #
    #     if auth.authenticate(request, username=username, password=password):
