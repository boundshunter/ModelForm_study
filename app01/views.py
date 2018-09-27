from django.shortcuts import render, HttpResponse, redirect
from django.forms import fields as Ffields
from django import forms
from django.forms import widgets as Fwidgets
from app01 import models

# Create your views here.


# class UserInfoForm(forms.Form):
#     username = fields.CharField(max_length=32)
#     email = fields.EmailField()
#     user_type = fields.ChoiceField(
#         choices=models.UserType.objects.values_list('id', 'caption')
#     )
#
#     def __init__(self, *args, **kwargs):
#         super(UserInfoForm, self).__init__(*args, **kwargs)
#         self.fields['user_type'].choices = models.UserType.objects.values_list('id', 'caption')

class UserInfoModelForm(forms.ModelForm):

    # 额外标签，免登陆选项，不需要提交数据库
    is_rmb = Ffields.CharField(widget=Fwidgets.CheckboxInput())

    class Meta:
        model = models.UserInfo
        fields = '__all__'
        labels = {
            'username': '用户名',
            'email': '邮箱',
            'user_type': '用户类型'
        }

        help_texts = {
            'username': '填写用户',
            'email': '填写邮箱',
            'user_type': '选择用户类型'
        }

        widgets = {
            'username': Fwidgets.Textarea(attrs={'class': 'c1'})
        }

        error_messages = {
            '__all__': {

            },
            'email': {
                'required': '邮箱不能为空',
                'invalid': '邮箱格式不正确',
            },
        }

        field_classes = {
            # 'email': Ffields.URLField,  # 修改正则判断字段的规则为URL模式
        }

        locallized_fileds = ('ctime',)  # 本地时区的设置根据settings.py中的TIME_ZONE = 'Asia/Shanghai'


def index(request):
    if request.method == 'GET':
        obj = UserInfoModelForm()
        return render(request, 'index.html', {'obj': obj})

    elif request.method == 'POST':
        obj = UserInfoModelForm(request.POST)
        if obj.is_valid():  # true
            obj.save()  # 提交数据正确，自动保存到数据库，做数据增加功能

            # obj.save() 等于下面流程
            # instance = obj.save(False) # Fasle什么都不做
            # instance.save()  # 只保存当前的操作，并不做多对多的关联操作
            # obj.save_m2m()  # 做多对多的关联操作


        print('STATUS:', obj.is_valid())
        print('DATA:', obj.cleaned_data)
        print('ERROR:', obj.errors.as_json())
        # 创建
        # models.UserInfo.objects.create(**obj.cleaned_data)
        # 更新
        # models.UserInfo.objects.filter(id=1).update(**obj.cleaned_data)
        return render(request, 'index.html', {'obj': obj})


def user_list(request):
    lst = models.UserInfo.objects.all().select_related('user_type',)
    return render(request, 'user_list.html', {'lst': lst})


def user_edit(request, nid):
    # 获取当前id对应的数据
    # 显示用户默认存在的数据
    if request.method == 'GET':
        user_obj = models.UserInfo.objects.filter(id=nid).first()
        mf = UserInfoModelForm(instance=user_obj)
        return render(request, 'user_edit.html', {'mf': mf, 'nid': nid})
    elif request.method == 'POST':
        user_obj = models.UserInfo.objects.filter(id=nid).first()
        mf = UserInfoModelForm(request.POST, instance=user_obj)
        if mf.is_valid():
            mf.save()
        else:
            print(mf.errors.as_json())
        return render(request, 'user_edit.html', {'mf': mf, 'nid': nid})


def ajax(request):
    return render(request, 'ajax.html')


def ajax_json(request):
    import time
    # time.sleep(3)
    print(request.POST)
    ret = {'code': True, 'data': request.POST.get('username')}
    import json
    return HttpResponse(json.dumps(ret))


def upload(request):
    return render(request, 'upload.html')


def upload_file(request):
    username = request.POST.get('username')
    fafafa = request.POST.get('fafafa')
    import os
    img_path = os.path.join('static/imgs/', fafafa.name)
    with open(img_path, 'wb') as f:
        for item in fafafa.chunks():
           f.write(item)

    ret = {'code': True, 'data': img_path}
    import json
    return HttpResponse(json.dumps(ret))
