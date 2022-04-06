from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from api.models import Subject, Assignment, Account, Score
from rest_framework.authtoken.models import Token
import pickle, os, json
import requests
import api_urls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'home.html')

## Page Assignment student mode ##

@login_required
def subject_list(request):
    subject = Account.objects.all().filter(user=request.user).values_list('idSubject')
    reloaded_subject = Account.objects.all()
    reloaded_subject.query = pickle.loads(pickle.dumps(subject.query))
    subject = []
    for item in reloaded_subject:
        item = item['idSubject'].upper()
        subject.append(item)
    return render(request, 'subject_list.html',{
        'assigns': subject
    })

@login_required
def assign_list(request, subject):
    assign = Assignment.objects.filter(idSubject=subject).values_list('idSubject', 'assignment', 'language')
    reloaded_assign = Account.objects.all()
    reloaded_assign.query = pickle.loads(pickle.dumps(assign.query))
    return render(request, 'assign_list.html',{
        'assigns': reloaded_assign
    })

@login_required
def assign_score(request, subject, assign):
    score = Score.objects.filter(user=request.user ,idSubject=subject, assignment=assign).values_list('idSubject', 'assignment', 'score', 'check' ,'timeIn', 'error')
    reloaded_score = Account.objects.all()
    reloaded_score.query = pickle.loads(pickle.dumps(score.query))
    return render(request, 'assign_score.html',{
        'assigns': reloaded_score,
        'subject': subject
    })

@login_required
def upload_assign(request, subject, assign):
    if request.method == 'POST':
        assignment = Assignment.objects.get(idSubject=subject, assignment=assign)
        files = []
        values = {
            'subjectId': subject,
            'assignId': assign,
            'language': assignment.language,
        }
        if 'fileAssignment' in request.FILES:
            files.append(('fileAssignment',request.FILES['fileAssignment']))
        if 'otherFiles' in request.FILES:
            for file in request.FILES.getlist('otherFiles'):
                files.append(('otherFiles',file))
        token, _ = Token.objects.get_or_create(user=request.user)
        res = requests.request("POST", api_urls.URL_RESTAPI_COMPILE, headers={'Authorization': f'Token {token}'}, data=values, files=files)
        assign = Assignment.objects.filter(idSubject=subject).values_list('idSubject', 'assignment', 'language')
        reloaded_assign = Account.objects.all()
        reloaded_assign.query = pickle.loads(pickle.dumps(assign.query))
        return render(request, 'assign_list.html',{
                'assigns': reloaded_assign,
                'error' : res.text
            })

## Page Assignment instructor mode ##

@login_required
def subject_list_instructor(request):
    subject = Account.objects.all().filter(user=request.user).values_list('idSubject')
    reloaded_subject = Account.objects.all()
    reloaded_subject.query = pickle.loads(pickle.dumps(subject.query))
    subject = []
    for item in reloaded_subject:
        item = item['idSubject'].upper()
        subject.append(item)
    return render(request, 'subject_list_problem_instructor.html',{
        'assigns': subject
    })

@login_required
def assign_list_instructor(request, subject):
    assign = Assignment.objects.filter(idSubject=subject).values_list('idSubject', 'assignment', 'language')
    reloaded_assign = Account.objects.all()
    reloaded_assign.query = pickle.loads(pickle.dumps(assign.query))
    return render(request, 'assign_list_instructor.html',{
        'assigns': reloaded_assign,
        'subject': subject
    })


@login_required
def assign_student_list(request, subject, assign):
    account = Account.objects.filter(idSubject=subject).values_list('user_id')
    reloaded_account = Account.objects.all()
    reloaded_account.query = pickle.loads(pickle.dumps(account.query))
    username = []
    score_list = []
    for user_id in reloaded_account:
        student = User.objects.get(id=user_id['user_id'])
        username.append(student.username)
        score = Score.objects.filter(user=student.id ,idSubject=subject, assignment=assign).values_list('score', flat=True).order_by('score').first()
        if score is None:
            score = 0.0
        score_list.append(score)
        
    return render(request, 'student_list.html',{
        'students': list(zip(username, score_list)),
        'subject': subject,
        'assignId': assign
    })

@login_required
def assign_student_score(request, subject, assign, id):
    user = User.objects.get(username=id).id
    score = Score.objects.filter(user=user ,idSubject=subject, assignment=assign).values_list('idSubject', 'assignment', 'score', 'check' ,'timeIn', 'error')
    reloaded_score = Account.objects.all()
    reloaded_score.query = pickle.loads(pickle.dumps(score.query))
    return render(request, 'assign_student_score.html',{
        'scores': reloaded_score,
        'subject': subject,
        'assign': assign,
        'student': id,
    })


  ## Page Problem instructor mode ##

@login_required
def subject_list_problem(request):
    subject = Account.objects.all().filter(user=request.user).values_list('idSubject')
    reloaded_subject = Account.objects.all()
    reloaded_subject.query = pickle.loads(pickle.dumps(subject.query))
    subject = []
    for item in reloaded_subject:
        item = item['idSubject'].upper()
        subject.append(item)
    return render(request, 'subject_list_problem.html',{
        'assigns': subject
    })

@login_required
def problem_list(request, subject):
    assign = Assignment.objects.filter(idSubject=subject).values_list('idSubject', 'assignment', 'language')
    reloaded_assign = Account.objects.all()
    reloaded_assign.query = pickle.loads(pickle.dumps(assign.query))
    return render(request, 'problem_list.html',{
        'assigns': reloaded_assign,
        'subject': subject
    })

@login_required
def problem_detail(request, subject, assign):
    detail = Assignment.objects.get(idSubject=subject, assignment=assign)
    itemInput = os.listdir(detail.pathInput)
    itemOutput = os.listdir(detail.pathOutput)
    if os.path.exists(detail.result):
        result = open(detail.result, "r")
        result = json.load(result)
        result.keys()
        result.values()
        result = list(zip(result.keys(), result.values()))
    else: result = False
    return render(request, 'problem_detail.html',{
        'assigns': detail,
        'ItemInOuts': list(zip(itemInput, itemOutput)),
        'result': result,
    })

@login_required
def problem_delete(request, subject, assign):
    assignment = Assignment.objects.filter(idSubject=subject).values_list('idSubject', 'assignment', 'language')
    reloaded_assign = Account.objects.all()
    reloaded_assign.query = pickle.loads(pickle.dumps(assignment.query))
    token, _ = Token.objects.get_or_create(user=request.user)
    params = {
            'subjectId': subject,
            'assignId': assign,
        }
    res = requests.delete(api_urls.URL_RESTAPI_PROBLEM, headers={'Authorization': f'Token {token}'}, params=params)
    return render(request, 'problem_list.html',{
        'assigns': reloaded_assign,
        'subject': subject,
        'error': res.text
        })

@login_required
def problem_create(request, subject):
    if request.method == 'GET':
        return render(request, 'problem_create.html',{
            'subject': subject
        })
    if request.method == 'POST':
        token, _ = Token.objects.get_or_create(user=request.user)
        files = []
        payload = {'subjectId': subject,}
        headers = {
        'Authorization': f'Token {token}'
        }
        if 'assignId' in request.POST:
            payload['assignId'] = request.POST['assignId']
        if 'language' in request.POST:
            payload['language'] = request.POST['language']
        if 'format' in request.POST:
            payload['format'] = request.POST['format']
        if 'format' in request.POST:
            payload['format'] = request.POST['format']
        if 'fileAssignment' in request.FILES:
            files.append(('fileAssignment',request.FILES['fileAssignment']))
        if 'filesInput' in request.FILES:
            for file in request.FILES.getlist('filesInput'):
                files.append(('filesInput',file))
        if 'filesOutput' in request.FILES:
            for file in request.FILES.getlist('filesOutput'):
                files.append(('filesOutput',file))
        if 'otherFiles' in request.FILES:
            for file in request.FILES.getlist('otherFiles'):
                files.append(('otherFiles',file))
        response = requests.request("POST", api_urls.URL_RESTAPI_PROBLEM, headers=headers, data=payload, files=files)
        response = json.loads(response.content)
        if 'error' in response:
            return render(request, 'problem_create.html',{
                'subject': subject,
                'error': response['error'],
            })
        elif 'Queue' in response:
            status = list(response['Queue'].values())
            if not status[0]:
                return render(request, 'problem_create.html',{
                    'subject': subject,
                    'error': status[2],
                })
            else: return redirect('problem_list' , subject=subject)

@login_required
def problem_edit(request, subject, assign):
    if request.method == 'GET':
        return render(request, 'problem_edit.html',{
            'subject': subject,
            'assign': assign
        })
    if request.method == 'POST':
        assignment = Assignment.objects.get(idSubject=subject, assignment=assign)
        token, _ = Token.objects.get_or_create(user=request.user)
        files = []
        payload = {
            'subjectId': subject,
            'assignId': assign,
            'language': assignment.language,
            'format': assignment.format,
            }
        headers = {
        'Authorization': f'Token {token}'
        }
        if 'fileAssignment' in request.FILES:
            files.append(('fileAssignment',request.FILES['fileAssignment']))
        if 'filesInput' in request.FILES:
            for file in request.FILES.getlist('filesInput'):
                files.append(('filesInput',file))
        if 'filesOutput' in request.FILES:
            for file in request.FILES.getlist('filesOutput'):
                files.append(('filesOutput',file))
        if 'otherFiles' in request.FILES:
            for file in request.FILES.getlist('otherFiles'):
                files.append(('otherFiles',file))
        response = requests.request("PUT", api_urls.URL_RESTAPI_PROBLEM, headers=headers, data=payload, files=files)
        response = json.loads(response.content)
        if 'error' in response:
            return render(request, 'problem_edit.html',{
                'subject': subject,
                'assign': assign,
                'error': response['error'],
            })
        elif 'Queue' in response:
            status = list(response['Queue'].values())
            if not status[0]:
                return render(request, 'problem_edit.html',{
                    'subject': subject,
                    'assign': assign,
                    'error': status[2],
                })
            else: return redirect('problem_list' , subject=subject)