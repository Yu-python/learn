import random, json
from io import BytesIO

from captcha.image import ImageCaptcha
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from . import blog_form
from . import models
from django.db.models import F
from bs4 import BeautifulSoup


# Create your views here.


# 注册
class Register(View):

    def get(self, request, *args, **kwargs):
        print(request.GET)
        register_form = blog_form.Register()
        return render(request, 'register.html', locals())

    def post(self, request, *args, **kwargs):

        from django.core.handlers.wsgi import WSGIRequest
        register_form = blog_form.Register(request.POST)
        msg = {'code': 200, 'msg': None}
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            head = request.FILES.get('head')
            models.User.objects.create_user(username=username, password=password, head=head)
            msg['msg'] = '注册成功'
            msg['url'] = '/blog/login/'
        else:
            msg.update(register_form.errors)
            msg['code'] = 100
        return JsonResponse(msg)


# 登录
class Login(View):
    def get(self, request, *args, **kwargs):
        login_form = blog_form.Login()
        return render(request, 'login.html', locals())

    def post(self, request, *args, **kwargs):
        print(request.POST)
        login_form = blog_form.Login(request.POST)
        msg = {'code': 200, 'msg': ''}
        check_code = request.POST.get('check_code')
        print(check_code)
        code = request.session.get('code')
        if check_code.lower() == code.lower():
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                print(username)
                user_obj = auth.authenticate(request, username=username, password=password)
                if user_obj:
                    auth.login(request, user_obj)
                    msg['msg'] = '登录成功'
                    msg['href'] = '/blog/index/'
                else:
                    msg['msg'] = '用户名或者密码错误'
                    msg['code'] = 100
            else:
                msg['code'] = 100
                msg['msg'] = login_form.errors
        else:
            msg['code'] = 100
            msg['msg'] = '验证码错误'
        return JsonResponse(msg)


# 验证码校验
class CheckCode(View):

    def get(self, request):
        # 验证码
        def generate_code(n=4):
            code = ''
            for i in range(n):
                # 小写字符
                lower_character = chr(random.randint(97, 122))
                # 大写字符
                upper_character = chr(random.randint(65, 90))
                # 数字
                number = random.randint(0, 9)
                # 合并一起
                code += str(random.choice([lower_character, upper_character, number]))
            return code

        code = generate_code()
        image = ImageCaptcha(width=115, height=38, font_sizes=(30, 30, 30)).generate_image(code)

        request.session['code'] = code

        print(request.session.get('code'))
        f = BytesIO()
        image.save(f, 'png')
        data = f.getvalue()
        return HttpResponse(data)


# 首页
class Index(View):
    def get(self, request, *args, **kwargs):
        article = models.Article.objects.all()
        return render(request, 'index.html', locals())


# 检查用户是否存在
class CheckUser(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        msg = {'code': 200, 'msg': 'None'}
        username = request.GET.get('username')
        res = models.User.objects.filter(username=username)
        print(res)
        if models.User.objects.filter(username=username):
            msg['code'] = 100
            msg['msg'] = '用户已经注册过了'
            return JsonResponse(msg)
        else:
            msg = {'code': 200}
            return JsonResponse(msg)


@method_decorator(login_required(login_url='/blog/login/'), name='get')
class Logout(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('/blog/index/')


# 修改头像像
class ChangeHead(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.head = request.FILES.get('head')
        user.save()
        msg = {'code': 200, "msg": "图片修改成功"}
        return JsonResponse(msg)


# 修改密码
class ChangePassword(View):

    def post(self, request, *args, **kwargs):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        msg = {'code': 200, 'msg': None}
        print(new_password, re_password, 11)
        if request.user.check_password(old_password):
            if new_password and re_password:
                if new_password == re_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    msg['code'] = 200
                    msg['msg'] = '密码修改成功'

                else:
                    msg['code'] = 100
                    msg['msg'] = '两次密码不一致'
            else:
                msg['code'] = 100
                msg['msg'] = '密码或者确密码不能为空'
        else:
            msg['code'] = 100
            msg['msg'] = '旧密码错误'
        return JsonResponse(msg)


# 用户首页，多核一
class UserIndex(View):
    def get(self, request, username, **kwargs):
        print(kwargs)

        if kwargs.get('date') == 'date':
            year, month = kwargs.get('other').split('-')
            user_article = models.Article.objects.filter(blog__user__username=username, create_time__year=year,
                                                         create_time__month=month)
            print(user_article, 'date')
        elif kwargs.get('tag') == 'tag':
            tag = kwargs.get('other')
            user_article = models.Article.objects.filter(blog__user__username=username, tag__tag__name=tag)
            print(user_article, 'tag')
        elif kwargs.get('category') == 'category':
            category = kwargs.get('other')
            user_article = models.Article.objects.filter(blog__user__username=username, category__name=category)
            print(user_article, 'category')
        else:
            user_article = models.Article.objects.filter(blog__user__username=username)
            print(user_article, '用户名')
        return render(request, 'userinfo.html', locals())

    def post(self, request, *args, **kwargs):
        pass


# 文章详情

class UserDetail(View):
    def get(self, request, username, pk, *args, **kwargs):
        user_obj = models.Article.objects.filter(blog__user__username=username, pk=pk).last()
        comment_list = models.Comment.objects.filter(article_id=user_obj.pk)
        return render(request, 'user_detail.html', locals())


class UpDown(View):

    def post(self, request, *args, **kwargs):
        msg = {'code': 200, 'msg': None}
        if request.user.is_authenticated:
            flag = request.POST.get('flag')
            flag = json.loads(flag)
            article_id = request.POST.get('article_id')
            if models.UpAndDown.objects.filter(user=request.user.username, article_id=article_id):
                msg['msg'] = '你已经点过了'
                msg['code'] = 100
            else:
                if flag:
                    models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                    msg['msg'] = '点赞成功了'
                    msg['flag'] = 1
                else:
                    models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                    msg['msg'] = '点踩成功'
                models.UpAndDown.objects.create(user=request.user, article_id=article_id, is_up=flag)

        else:
            msg['code'] = 100
            msg['msg'] = '你没有登录'
        return JsonResponse(msg)


class Admin(View):
    def get(self, request, *args, **kwargs):
        print(request.GET, 11111)
        article_obj = models.Article.objects.filter(blog=request.user.blog)
        category_obj = models.Category.objects.filter(blog=request.user.blog)
        tag_obj = models.Tag.objects.filter(blog=request.user.blog)
        return render(request, 'admin/admin.html', locals())

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tag = request.POST.getlist('tag')
        bs = BeautifulSoup(content, 'html.parser')
        desc = bs.text[0:90]
        res_script = bs.find_all('script')
        for script in res_script:
            script.decompose()
        res = models.Article.objects.create(title=title, description=desc, content=content, blog=request.user.blog,
                                            category_id=category)
        res.tag.set(tag)
        res.save()

        return redirect('/blog/admin/')


class Delete(View):
    def get(self, request, pk, *args, **kwargs):
        models.Article.objects.filter(pk=pk).delete()
        return redirect('/blog/admin/')


class Edit(View):
    def get(self, request, pk, *args, **kwargs):
        article_obj = models.Article.objects.get(pk=pk, blog=request.user.blog)
        tag = models.Tag.objects.filter(blog=request.user.blog)
        category = models.Category.objects.filter(blog=request.user.blog)
        print(article_obj)
        print(category)
        print(tag)
        return render(request, 'admin/edit.html', locals())

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        print(pk)
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tag = request.POST.getlist('tag')
        bs = BeautifulSoup(content, 'html.parser')
        desc = bs.text[0:90]
        res_script = bs.find_all('script')
        for script in res_script:
            script.decompose()
        models.Article.objects.filter(pk=pk).update(title=title, description=desc, content=content,
                                                    blog=request.user.blog,
                                                    category_id=category)
        res = models.Article.objects.get(pk=pk)
        res.tag.set(tag)
        res.save()

        return redirect('/blog/admin/')


class UploadImg(View):

    def post(self, request, *args, **kwargs):
        msg1 = {
            "error": 0,
            "url": "http://www.example.com/path/to/file.ext"
        }

        msg2 = {
            "error": 1,
            "message": "错误信息"
        }

        myfile = request.FILES.get('myfile')
        if myfile:
            import os
            from django.conf import settings

            path1 = os.path.join('static', 'img', myfile.name)
            path = os.path.join(settings.BASE_DIR, path1)
            with open(path, 'wb') as f:
                for line in myfile:
                    f.write(line)
                    msg1['url'] = 'http://127.0.0.1:8000/' + path1
                    print(path1, 11111111)
        else:
            msg1 = msg2
        return JsonResponse(msg1)



def comment(request, *args, **kwargs):
    res = {'code': 100, 'msg': ''}
    if request.is_ajax():
        article_id = request.POST.get('article_id')
        print(article_id,111111)
        content = request.POST.get('content')
        parent = request.POST.get('parent')
        if request.user.is_authenticated:
            article = models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                                   Comment_id_id=parent)
            models.Article.objects.filter(pk=article_id).update(commit_num=F('commit_num') + 1)
            res['msg'] = '评论成功'
            res['username'] = article.user.username

            res['content'] = article.content
            print(type(article))
            if parent:

                res['parent_name'] = article.Comment_id.user

            # # 发送邮件(同步操作)
            # from django.core.mail import send_mail
            # # send_mail('您的文章:%s被评论了'%'git从入门到放弃','%s评论了%s'%(request.user.username,'写的真好'),settings.EMAIL_HOST_USER,
            # #                                      ["1063926627@qq.com",'laichuangdelaoji@gmail.com'])
            # # 通过多线程,异步操作
            # from threading import Thread
            # t = Thread(target=send_mail, args=(
            # '您的文章:%s被评论了' % 'git从入门到放弃', '%s评论了%s' % (request.user.username, '写的真好'), settings.EMAIL_HOST_USER,
            # ["1063926627@qq.com", 'laichuangdelaoji@gmail.com']))
            # t.start()
        else:
            res['code'] = 109
            res['msg'] = '请先登录'

    return JsonResponse(res)
