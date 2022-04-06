from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.views.decorators.csrf import csrf_exempt

from frontApi import views

urlpatterns = [
    path("", views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),

    ## Page Assignment student mode ##
    path("assign/", views.subject_list, name="subject_list"),
    path("assign/<str:subject>/", views.assign_list, name="assign_list"),
    path("assign/<str:subject>/<str:assign>/", views.assign_score, name="assign_score"),
    path("assign/<str:subject>/<str:assign>/upload/", views.upload_assign, name="upload_assign"),

    ## Page Assignment instructor mode ##
    path("instructor/", views.subject_list_instructor, name="subject_list_instructor"),
    path("instructor/<str:subject>/", views.assign_list_instructor, name="assign_list_instructor"),
    path("instructor/student/<str:subject>/<str:assign>/", views.assign_student_list, name="assign_student_list"),
    path("instructor/student/<str:subject>/<str:assign>/<str:id>/", views.assign_student_score, name="assign_student_score"),

    ## Page Problem instructor mode ##
    path("problem/", views.subject_list_problem, name="subject_list_problem"),
    path("problem/<str:subject>/", views.problem_list, name="problem_list"),
    path("problem/<str:subject>/create/", views.problem_create, name="problem_create"),
    path("problem/<str:subject>/<str:assign>/", views.problem_detail, name="problem_detail"),
    path("problem/<str:subject>/<str:assign>/delete/", views.problem_delete, name="problem_delete"),
    path("problem/<str:subject>/<str:assign>/edit/", views.problem_edit, name="problem_edit"),
    # path("problem/", views.problem_list, name="problem_list"),
    # path("problem/upload", views.upload_problem, name="upload_problem"),
    # path("problem/update/<int:pk>/", views.update_problem, name="update_problem"),
    # path("problem/<int:pk>/", views.delete_problem, name="delete_problem"),
]