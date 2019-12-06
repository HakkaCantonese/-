from django.urls import path,include
from django.conf.urls import url
from django.contrib import admin
from . import  views

urlpatterns = [
    url(r'^check_code.html$',views.check_code),
    path('logingate/',views.loginproc),
    path("logintest/",views.dologin),
    path('logout/',views.logout),
    path('view1/',views.view1),
    path('view2/',views.view2),
    path('view3/',views.view3),
    path('view4_1/', views.view4_1),
    path('view4_2/', views.view4_2),
    path('view4_3/', views.view4_3),
    path('admin/', admin.site.urls),
    path('captcha/',include('captcha.urls')),
]