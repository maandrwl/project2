from ast import If
from contextlib import redirect_stderr
import imp
from multiprocessing import context
from turtle import title
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import ItemForm, AssignForm
from .decorators import allowed_users, unauthenticated_user, admin_only
from django.core.paginator import Paginator

#Admin and Teacher homepage
@login_required
@admin_only
def home(request):
    count = User.objects.count()
    return render(request,'home.html',{
        'count': count
    })


#Assignment from teacher site
@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def asteacher(request):
    assign = Assign.objects.all().order_by('-date_created')
    return render(request,'assignment-t.html',{'assign':assign})

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def create(request):

    form = AssignForm()
    if request.method == 'POST' :
        #print('Printing POST:', request.POST)
        form = AssignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/assignment-t','/assignment')
    context = {'form': form}

    #if request.method == 'POST':
        #upload_file = request.FILES['document']
        #fs = FileSystemStorage()
        #fs.save(upload_file.name, upload_file)
        #print(uploaded_file.name)
        #print(uploaded_file.size)
    return render(request,'createassign.html',context)

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def updateassign(request, pk):

    assign = Assign.objects.get(id=pk)
    form = AssignForm(instance=assign)

    if request.method == 'POST' :
        form = AssignForm(request.POST, instance=assign)
        if form.is_valid():
            form.save()
            return redirect('/assignment-t','/assignment')
    context = {'form': form}
    return render(request,'createassign.html',context)

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def deleteassign(request, pk):

    assign = Assign.objects.get(id=pk)
    if request.method == 'POST' :
        assign.delete()
        return redirect('/assignment-t','/assignment')

    context = {'item':assign}
    return render(request,'deleteassign.html', context)




#Course from teacher site
@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def subject(request):
    if 's' in request.GET:
        s = request.GET['s']
        subject = Item.objects.filter(CourseName__icontains=s)
    else:
        subject = Item.objects.all().order_by('CourseName')
    
    #paginator=Paginator(subject,2)
    #page_number=request.GET.get('page')
    #subject=paginator.get_page(page_number)

    #subject = Item.objects.all().order_by('CourseName')
    return render(request,'course-t.html',{'subject':subject})

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def createcourse(request):

    form = ItemForm()
    if request.method == 'POST' :
        #print('Printing POST:', request.POST)
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/course-t','/course')
    context = {'form': form}
    return render(request,'newcourse.html',context)

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def updatecourse(request, pk):

    course = Item.objects.get(id=pk)
    form = ItemForm(instance=course)

    if request.method == 'POST' :
        form = ItemForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('/course-t','/course')

    context = {'form': form}
    return render(request,'newcourse.html',context)

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def deletecourse(request, pk):

    course = Item.objects.get(id=pk)
    if request.method == 'POST' :
        course.delete()
        return redirect('/course-t','/course')

    context = {'item':course}
    return render(request,'deletecourse.html', context)

@login_required
@allowed_users(allowed_roles=['admin','teacher'])
def score(request):
    return render(request,'editscore.html')


#Student Site
@login_required
@allowed_users(allowed_roles=['admin','student'])
def userPage(request):
    return render(request,'homeuser.html')

@login_required
@allowed_users(allowed_roles=['admin','student'])
def course(request):
    if 's' in request.GET:
        s = request.GET['s']
        subject = Item.objects.filter(CourseName__icontains=s)
    else:
        subject = Item.objects.all().order_by('CourseName')
    #subject = Item.objects.all().order_by('CourseName')
    return render(request,'course.html',{'subject':subject})

@login_required
@allowed_users(allowed_roles=['admin','student'])
def assignment(request):
    assign = Assign.objects.all().order_by('-date_created')
    return render(request,'assignment.html',{'assign':assign})

@login_required
@allowed_users(allowed_roles=['admin','student'])
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        return redirect('/assignment')

    return render(request,'upload.html', context)

@login_required
@allowed_users(allowed_roles=['admin','student'])
def viewscore(request):
    assign = Assign.objects.all().order_by('-date_created')
    return render(request,'viewscore.html',{'assign':assign})

@login_required
@allowed_users(allowed_roles=['admin','student'])
def myprofile(request):
    return render(request,'profile.html')


#@unauthenticated_user
#def signup(request):
    #if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        #if form.is_valid():
            #user = form.save()
            #return redirect('home')
    #else:
        #form = UserCreationForm()
    #return render(request,'registration/signup.html',{
        #'form': form
    #})