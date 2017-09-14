# -*- coding: utf-8 -*-
# @Author: bxsh
# @Email:  xbc0809@gmail.com
# @File:  forms.py
# @Date:  2017/8/31 18:13

from django import forms


class LoginForm(forms.Form):
    user_id = forms.CharField(label='用户名：', widget=forms.TextInput(attrs={'placeholder': '用户名', 'class': 'inputs'}),
                              required=True,
                              error_messages={'required': '用户名不能为空'}, )
    pass_word = forms.CharField(label='密码：', widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'inputs'}),
                                required=True,
                                error_messages={'required': '密码不能为空'})


class Regist(forms.Form):
    user_id = forms.CharField(label='用户名：', widget=forms.TextInput(attrs={'placeholder': '用户名', 'class': 'inputs'}),
                              required=True,
                              error_messages={'required': '用户名不能为空'})
    pass_word = forms.CharField(label='密码：',
                                widget=forms.PasswordInput(attrs={'placeholder': '密码（字母、数字，至少6位）', 'class': 'inputs'}),
                                required=True,
                                error_messages={'required': '密码不能为空'})
    re_pass_word = forms.CharField(label='请再次输入密码：',
                                   widget=forms.PasswordInput(
                                       attrs={'placeholder': '再次输入密码（字母、数字，至少6位）', 'class': 'inputs'}),
                                   required=True,
                                   error_messages={'required': '密码不能为空'})

    def clean(self):  # 自带的数据清理处理方法
        super(Regist, self).clean()
        password = self.cleaned_data.get('pass_word')
        confirm_password = self.cleaned_data.get('re_pass_word')
        if password and password != confirm_password:
            self._errors['pass_word'] = self.error_class([u'两次密码不匹配'])
        return self.cleaned_data


if __name__ == '__main__':
    pass
