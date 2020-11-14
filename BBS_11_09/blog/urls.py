from django.urls import path,re_path
from django.views.static import serve
from . import views
from django.conf import settings

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view()),
    path('check_code/', views.CheckCode.as_view()),
    path('index/', views.Index.as_view()),
    path('check_user/', views.CheckUser.as_view()),
    path('logout/', views.Logout.as_view()),
    path('change_password/', views.ChangePassword.as_view()),
    path('change_head/', views.ChangeHead.as_view()),
    path('up_down/', views.UpDown.as_view()),
    path('admin/', views.Admin.as_view()),
    path('comment/', views.comment),
    path('upload_img/', views.UploadImg.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', views.Delete.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$', views.Edit.as_view()),
    re_path(r'^(?P<username>\w+)/(?P<pk>\d+)/$', views.UserDetail.as_view()),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^(?P<username>\w+)/(?P<data>(date|tag|category))/(?P<other>.*)/$', views.UserIndex.as_view()),
    re_path(r'^(?P<username>\w+)/$', views.UserIndex.as_view()),
    # re_path(r'^(?P<username>\w+)/', views.UserIndex.as_view()),

]
