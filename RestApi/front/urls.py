"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from front import views
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.home, name='home'),
    path("home/", views.userPage, name='homeuser'),
    #path("signup/", views.signup, name='signup'),
    path("accounts/", include('django.contrib.auth.urls')),
    path("course/", views.course),
    path("assignment/", views.assignment,name='assignstudent'),

    path("viewscore/", views.viewscore),
    
    path("editscore/", views.score),
    path("profile/", views.myprofile),

    path("course-t/", views.subject,name='subject'),
    
    path("assignment-t/", views.asteacher,name='assignteacher'),

    path("createassign/", views.create,name='create'),
    path("update_assign/<str:pk>", views.updateassign,name='update_assign'),
    path("delete_assign/<str:pk>", views.deleteassign,name='delete_assign'),
    path("course-t/<slug:slug>/", views.assignlist,name='assign_list'),

    path("newcourse/", views.createcourse,name='newcourse'),
    path("update_course/<str:pk>", views.updatecourse,name='update_course'),
    path("delete_course/<str:pk>", views.deletecourse,name='delete_course'),

    path("upload/", views.upload,name='upload'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)