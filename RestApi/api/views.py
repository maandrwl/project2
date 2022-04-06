from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST
# More rest imports as needed
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
from werkzeug.utils import secure_filename
import os
import json
import shutil
import requests
from .decorators import define_usage
from .models import Subject, Assignment, Account, Score
from django.contrib.auth.models import User, Group
from .serializers import scoreSerializer, accountSerializer, assignmentSerializer
import api_urls
import response_code
import defineUsage

#set BASE path ex. c://home//project
BASE = os.path.dirname(os.path.abspath(__file__))
BASE_dir = os.path.dirname(BASE)
#set name folder for storage subject, assignment and create directory
SUBJECT_DIR = 'Subject'
os.makedirs(os.path.join(BASE_dir, SUBJECT_DIR), exist_ok=True)
STUDENT_DIR = 'Student'
os.makedirs(os.path.join(BASE_dir, STUDENT_DIR), exist_ok=True)
STORE_DIR = 'store_output'
os.makedirs(os.path.join(BASE_dir, STORE_DIR), exist_ok=True)
#set urls
STAGE2 = api_urls.BASE_URL_STAGE2
apiFinal = os.path.join(api_urls.BASE_URL_RESTAPI, 'api/finalStage')

### use try and except because when run command python manage.py makemigrations. 
### File views.py run too, So use try and except for ignore command python manage.py makemigrations 
try:
    #Group for endpoint /problem
    if not Group.objects.filter(name='instructor').exists():
        group = Group(name = "instructor")
        group.save()

    subject = Subject.objects.all()
    for item in subject:
        subject_path = os.path.join(BASE_dir, SUBJECT_DIR, item.idSubject)
        os.makedirs(subject_path, exist_ok=True)
except:
    pass

#allowe type for file
ALLOWED_SOURCE_CODE = set(['py', 'java'])
def allowed_source_code(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_SOURCE_CODE
#allowe type for input and output
ALLOWED_EXTENSIONS = set(['txt'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#URL /
@define_usage(returns={'url_usage': 'Dict'})
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_index(requet):
    details = {}
    for item in list(globals().items()):
        if item[0][0:4] == 'api_':
            if hasattr(item[1], 'usage'):
                details[reverse(item[1].__name__)] = item[1].usage
    return Response(details)

#URL /signin/
@define_usage(params={'username': 'String', 'password': 'String'},
              returns={'authenticated': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signin(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except:
        return Response({'error': 'Please provide correct username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response({'authenticated': False, 'token': None})

#URL /compile/
@define_usage(params=defineUsage.compile_params,
              returns=defineUsage.compile_return)
@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_compile(request):
    #check error
    def validError():
        if not (language == 'java'   or language  == 'python' or language == 'py'):
            return response_code.COMPILE_STATUS_ERROR_1
        if not (fileAssignment and allowed_source_code(fileAssignment.name)):
            return response_code.COMPILE_STATUS_ERROR_2
        if subjectId not in validSubject:
            return response_code.COMPILE_STATUS_ERROR_3
        if assignId not in validAssignment:
            return response_code.COMPILE_STATUS_ERROR_4
        if not (os.listdir(os.path.join(BASE_dir, pathIn)) or os.listdir(os.path.join(BASE_dir, pathOut))):
            return response_code.COMPILE_STATUS_ERROR_5
        typefile = '.' in filename and filename.rsplit('.', 1)[1].lower()
        if not ((assign_lang == language) and (assign_lang == typefile)):
            return response_code.COMPILE_STATUS_ERROR_6
        else: return response_code.COMPILE_STATUS_OK

    if request.method == 'GET':
        if ('subjectId' in request.query_params) and ('assignId' in request.query_params):
            subjectId = request.query_params.get('subjectId').upper()
            assignId = request.query_params.get('assignId').upper()
            scores = scoreSerializer(request.user.score_set.filter(idSubject=subjectId, assignment=assignId), many=True)
            return Response({'Score': scores.data})
        if ('subjectId' in request.query_params):
            subjectId = request.query_params.get('subjectId').upper()
            scores = scoreSerializer(request.user.score_set.filter(idSubject=subjectId), many=True)
            return Response({'Score': scores.data})
        if 'assignId' in request.query_params:
            return Response({'error': 'Method get recive 3 pattern 1.null 2.feild subjectId 3.field subjectId and assignId'})
        elif request.query_params:
            return Response({'error': 'Method get recive 3 pattern 1.null 2.feild subjectId 3.field subjectId and assignId'})
        else:
            scores = scoreSerializer(request.user.score_set.all(), many=True)
            return Response({'Score': scores.data})
    if request.method == 'POST':
        time = datetime.datetime.now().strftime('%d-%m-%YT%H-%M-%S.%f')[:-3]
        if 'fileAssignment' not in request.FILES:
            return Response({'error': 'Field fileAssignment not found.'},
                            status=HTTP_400_BAD_REQUEST)
        if 'subjectId' not in request.data:
            return Response({'error': 'Field subjectId not found.'},
                            status=HTTP_400_BAD_REQUEST)
        if 'assignId' not in request.data:
            return Response({'error': 'Field assignId not found.'},
                            status=HTTP_400_BAD_REQUEST)
        if 'language' not in request.data:
            return Response({'error': 'Field language not found.'},
                            status=HTTP_400_BAD_REQUEST)
        if 'api' not in request.data:
            api = None
        else: api = request.data['api']
        
        fileAssignment = request.FILES['fileAssignment']
        subjectId = request.data['subjectId'].upper()
        assignId = request.data['assignId'].upper()
        language = request.data['language'].lower()
        if language == 'python':
            language = 'py'

        #check subject vaild in account
        validSubject = Account.objects.get(user=request.user).idSubject.values_list('idSubject' , flat = True)
        #check assignment vaild in subject
        assignment = Assignment.objects.all()
        validAssignment = assignment.filter(idSubject=subjectId).values_list('assignment' , flat = True)
        try:
            assignment = assignment.get(idSubject=subjectId, assignment=assignId)
            assign_lang = assignment.language
        except:
            pass
        if (subjectId in validSubject) and (assignId in validAssignment):
            pathIn = assignment.pathInput
            pathOut = assignment.pathOutput
        filename = secure_filename(fileAssignment.name)
        #check error
        status = validError()

        if status['Status']:
            path = os.path.join(subjectId, assignId, str(request.user), time)
            path_file = os.path.join(BASE_dir, STUDENT_DIR, path)
            os.makedirs(path_file)
            #save file
            default_storage.save(os.path.join(path_file, filename), ContentFile(fileAssignment.read()))
            if 'otherFiles' in request.FILES:
                for file in request.FILES.getlist('otherFiles'):
                    if file and allowed_source_code(file.name):
                        name = secure_filename(file.name)
                        default_storage.save(os.path.join(path_file, name), ContentFile(file.read()))
                    else:
                        return Response({'error': "Other Files isn't Java or Python."},
                                status=HTTP_400_BAD_REQUEST)
            #save database
            score = Score(user=request.user,
                idSubject=subjectId,
                assignment=assignId,
                timeIn=time,
                )
            score.save()

            #make data type dictionary for send to stage2
            data = {"problem": False,
                    "output": True,
                    "user": str(request.user),
                    "id": Score.objects.get(user=request.user, timeIn=time).id,
                    "data": {"filename": filename,
                            "pathFile": path_file,
                            "pathIn": os.path.join(BASE_dir, pathIn),
                            "pathOut": os.path.join(BASE_dir, pathOut),
                            "api": api,
                            "apiFinal": apiFinal,
                            "language": language,
                            "format": assignment.format,
                        },
                    "status":{"boolean":True,
                            "code":100,
                            "description":"OK"},
                        }
            #send request to stage2
            res = requests.post(STAGE2, json=data)
            res = json.loads(res.content)
            status['Queue'] = res
        return Response({'Queue': status})

#URL /problem/
@define_usage(params=defineUsage.problem_params,
              returns=defineUsage.problem_return)
@api_view(['GET','POST','DELETE','PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_problem(request):

    time = datetime.datetime.now().strftime('%d-%m-%YT%H-%M-%S.%f')[:-3]
    #check error
    def validError(sourceCode, inOut=True, PUT=False):
        #check PUT method
        if PUT:
            if subjectId not in validSubject:
                return response_code.PROBLEM_STATUS_ERROR_5
            if assignId not in validAssignment:
                return response_code.PROBLEM_STATUS_ERROR_6
            if ('filesInput' in request.FILES) != ('filesOutput' in request.FILES):
                if request.FILES.getlist('filesInput'):
                    #check file name in database
                    for file in request.FILES.getlist('filesInput'):
                        if file and allowed_file(file.name):
                            name = secure_filename(file.name)
                            if not os.path.exists(os.path.join(pathIn, name)):
                                return response_code.PROBLEM_STATUS_ERROR_9
                if request.FILES.getlist('filesOutput'):
                    #check file name in database
                    for file in request.FILES.getlist('filesOutput'):
                        if file and allowed_file(file.name):
                            name = secure_filename(file.name)
                            if not os.path.exists(os.path.join(pathOut, name)):
                                return response_code.PROBLEM_STATUS_ERROR_9
            else:
                #check number of file input and output is the equal or not
                if len(request.FILES.getlist('filesInput')) == len(request.FILES.getlist('filesOutput')):
                    listIn = []
                    #check name file input and output is match or not
                    for file in request.FILES.getlist('filesInput'):
                        nameFile = secure_filename(file.name)
                        listIn.append(nameFile)
                    for file in request.FILES.getlist('filesOutput'):
                        nameFile = secure_filename(file.name)
                        if nameFile not in listIn:
                            return response_code.PROBLEM_STATUS_ERROR_8
                else: return response_code.PROBLEM_STATUS_ERROR_7
        else:
            #check error type language
            if not (language == 'java' or language  == 'python' or language == 'py'):
                return response_code.PROBLEM_STATUS_ERROR_1
            #check error subject
            if subjectId not in validSubject:
                return response_code.PROBLEM_STATUS_ERROR_3
            #check error assignment
            if assignId in validAssignment:
                return response_code.PROBLEM_STATUS_ERROR_4
        #check number of file input and output is the equal or not
        #check name file input and output is match or not
        if inOut:
            if len(request.FILES.getlist('filesInput')) == len(request.FILES.getlist('filesOutput')):
                listIn = []
                for file in request.FILES.getlist('filesInput'):
                    nameFile = secure_filename(file.name)
                    listIn.append(nameFile)
                for file in request.FILES.getlist('filesOutput'):
                    nameFile = secure_filename(file.name)
                    if nameFile not in listIn:
                        return response_code.PROBLEM_STATUS_ERROR_8
            else: return response_code.PROBLEM_STATUS_ERROR_7
        #check error type file
        if sourceCode:
            if not (fileAssignment and allowed_source_code(fileAssignment.name)):
                return response_code.PROBLEM_STATUS_ERROR_2
        return response_code.PROBLEM_STATUS_OK

    #use for save file input
    def storeFileInput():
        os.makedirs(pathIn, exist_ok=True)
        if 'filesInput' in request.FILES:
            for file in request.FILES.getlist('filesInput'):
                if file and allowed_file(file.name):
                    name = secure_filename(file.name)
                    if os.path.exists(os.path.join(pathIn, name)):
                        newName = time + name
                        shutil.move(os.path.join(pathIn, name), os.path.join(path_outdated, newName))
                    default_storage.save(os.path.join(pathIn, name), ContentFile(file.read()))
                else: return Response({'error': "field filesInput must be .txt"},
                        status=HTTP_400_BAD_REQUEST)
    #use for save file output
    def storeFileOutput():
        os.makedirs(pathOut, exist_ok=True)
        if 'filesOutput' in request.FILES:
            for file in request.FILES.getlist('filesOutput'):
                if file and allowed_file(file.name):
                    name = secure_filename(file.name)
                    if os.path.exists(os.path.join(pathOut, name)):
                        newName = time + name
                        shutil.move(os.path.join(pathOut, name), os.path.join(path_outdated, newName))
                    default_storage.save(os.path.join(pathOut, name), ContentFile(file.read()))
                else: return Response({'error': "field filesOutput must be .txt"},
                        status=HTTP_400_BAD_REQUEST)
        else: print("field filesInput no exists.")
    #use for save main file
    def storeFileMain():
        if os.path.exists(os.path.join(path_file, filename)):
            newName = time + filename
            shutil.move(os.path.join(path_file, filename), os.path.join(path_outdated, newName))
        default_storage.save(os.path.join(path_file, filename), ContentFile(fileAssignment.read()))

    #set data type dictionary
    def dictdata():
        data = {"problem": True,
                "user": str(request.user),
                "id": Assignment.objects.get(idSubject=subjectId, assignment=assignId).id,
                "data": {"filename": filename,
                        "pathFile": path_file,
                        "pathAssignment": path_assignment,
                        "pathIn": pathIn,
                        "pathOut": pathOut,
                        "api": api,
                        "apiFinal": apiFinal,
                        "language": language,
                        "format": assignment.format,
                    },
                "status":{"boolean":True,
                        "code":200,
                        "description":"OK"},
                    }
        return data
        
    if request.user.groups.filter(name='instructor').exists():
        if request.method == 'GET':
            if ('subjectId' in request.query_params) and ('assignId' in request.query_params):
                subjectId = request.query_params.get('subjectId').upper()
                assignId = request.query_params.get('assignId').upper()
                assignment = Assignment.objects.get(idSubject=subjectId, assignment=assignId)
                score = assignment.score
                itemInput = os.listdir(assignment.pathInput)
                itemOutput = os.listdir(assignment.pathOutput)
                result = open(assignment.result, "r")
                return Response({
                    'Subject': subjectId,
                    'Assignment':assignId,
                    'Score':score,
                    'Files Input':itemInput,
                    'Files Output':itemOutput,
                    'Result':json.load(result),
                    }
                )
            if ('subjectId' in request.query_params):
                subjectId = request.query_params.get('subjectId').upper()
                subject = assignmentSerializer(Assignment.objects.all().filter(idSubject=subjectId), many=True)
                return Response({'Assignment': subject.data})
            if 'assignId' in request.query_params:
                return Response({'error': 'Method get recive 3 pattern 1.null 2.feild subjectId 3.field subjectId and assignId'})
            elif request.query_params:
                return Response({'error': 'Method get recive 3 pattern 1.null 2.feild subjectId 3.field subjectId and assignId'})
            else:
                subject = accountSerializer(Account.objects.filter(user=request.user), many=True)
                return Response(subject.data)
        if request.method == 'POST':
            if 'subjectId' not in request.data:
                return Response({'error': 'Field subjectId not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'assignId' not in request.data:
                return Response({'error': 'Field assignId not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'language' not in request.data:
                return Response({'error': 'Field language not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'api' not in request.data:
                api = None
            else: api = request.data['api']
            if 'format' not in request.data:
                return Response({'error': 'Field format not found.'},
                                status=HTTP_400_BAD_REQUEST)
            subjectId = request.data['subjectId'].upper()
            assignId = request.data['assignId'].upper()
            language = request.data['language'].lower()
            if language == 'python':
                language = 'py'
            formatAnswer = request.data['format'].lower()
            if formatAnswer == 'true':
                formatAnswer = True
            elif formatAnswer == 'false':
                formatAnswer = False
            else:
                return response_code.PROBLEM_STATUS_ERROR_10

            #set path
            #half path assignment
            path_assignment = os.path.join(SUBJECT_DIR, subjectId, assignId)
            #Full path file
            path_file = os.path.join(BASE_dir, path_assignment)
            #half path input assignment
            pathIn_save = os.path.join(path_assignment, "input")
            #half path output assignment
            pathOut_save = os.path.join(path_assignment, "output")
            #Full path outdated
            path_outdated = os.path.join(path_file, "outdated")
            #Full path input assignment
            pathIn = os.path.join(BASE_dir, pathIn_save)
            #Full path output assignment
            pathOut = os.path.join(BASE_dir, pathOut_save)

            #check subject vaild in account
            validSubject = Account.objects.get(user=request.user).idSubject.values_list('idSubject' , flat = True)
            #check assignmrnt vaild in subject
            validAssignment = Assignment.objects.all().filter(idSubject=subjectId).values_list('assignment' , flat = True)
            
            if ('fileAssignment' in request.FILES) and ('filesInput' in request.FILES) and ('filesOutput' in request.FILES):
                fileAssignment = request.FILES['fileAssignment']
                #check error
                status = validError(True)
                if status['Status']:
                    filename = secure_filename(fileAssignment.name)
                    if 'otherFiles' in request.FILES:
                        for file in request.FILES.getlist('otherFiles'):
                            if file and allowed_source_code(file.name):
                                name = secure_filename(file.name)
                                default_storage.save(os.path.join(path_assignment, name), ContentFile(file.read()))
                            else:
                                return Response({'error': "Other Files isn't Java or Python."},
                                        status=HTTP_400_BAD_REQUEST)
                    storeFileMain()

                    # storage input files
                    storeFileInput()
                    
                    # #storage output files
                    storeFileOutput()
                    #save data  to database
                    assignment = Assignment(idSubject=Subject.objects.get(idSubject=subjectId),
                                        assignment=assignId,
                                        pathMainFile = filename,
                                        pathInput=pathIn_save,
                                        pathOutput=pathOut_save,
                                        format = formatAnswer,
                                        language = language,
                                        )
                    assignment.save()
                    #call def dictdata
                    data = dictdata()
                    #send request to stage2
                    res = requests.post(STAGE2, json=data)
                    res = json.loads(res.content)
                    status['Queue'] = res
            elif ('fileAssignment' in request.FILES) and ('filesInput' in request.FILES) and ('filesOutput' not in request.FILES):
                fileAssignment = request.FILES['fileAssignment']
                #check error
                status = validError(True, inOut=False)

                if status['Status']:
                    filename = secure_filename(fileAssignment.name)
                    if 'otherFiles' in request.FILES:
                        for file in request.FILES.getlist('otherFiles'):
                            if file and allowed_source_code(file.name):
                                name = secure_filename(file.name)
                                default_storage.save(os.path.join(path_assignment, name), ContentFile(file.read()))
                            else:
                                return Response({'error': "Other Files isn't Java or Python."},
                                        status=HTTP_400_BAD_REQUEST)
                    storeFileMain()

                    #storage input files
                    storeFileInput()
                    os.makedirs(pathOut, exist_ok=True)
                    #save data  to database
                    assignment = Assignment(idSubject=Subject.objects.get(idSubject=subjectId),
                                        assignment=assignId,
                                        pathMainFile = filename,
                                        pathInput=pathIn_save,
                                        pathOutput=pathOut_save,
                                        format = formatAnswer,
                                        language = language,
                                        )
                    assignment.save()
                    #call def dictdata
                    data = dictdata()

                    #send request to stage2
                    res = requests.post(STAGE2, json=data)
                    res = json.loads(res.content)
                    status['Queue'] = res
            elif ('fileAssignment' not in request.FILES) and ('filesOutput' in request.FILES) and ('filesInput' in request.FILES) :
                #check error
                status = validError(False)

                if status['Status']:
                    #storage input files
                    storeFileInput()
                    
                    #storage output files
                    storeFileOutput()

                    #save data to database
                    assignment = Assignment(idSubject=Subject.objects.get(idSubject=subjectId),
                                        assignment=assignId,
                                        pathInput=pathIn_save,
                                        pathOutput=pathOut_save,
                                        format = formatAnswer,
                                        error = False,
                                        language = language,
                                        )
                    assignment.save()
                    return Response({'result': 'Create assignment without source code success'})
            else:
                return Response({'error': {'There are 3 forms of field file':{'1':'fileAssignment, filesInput, filesOutput','2':'fileAssignment, filesInput','3':'filesOutput, filesInput',},}},
                                status=HTTP_400_BAD_REQUEST)
            return Response({'Queue': status})
        if request.method == 'DELETE':
            if 'subjectId' not in request.query_params:
                return Response({'error': 'Field subjectId not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'assignId' not in request.query_params:
                return Response({'error': 'Field assignId not found.'},
                                status=HTTP_400_BAD_REQUEST)
            subjectId = request.query_params.get('subjectId').upper()
            assignId = request.query_params.get('assignId').upper()
            try:
                assignment = Assignment.objects.get(idSubject=subjectId, assignment=assignId)
                try:
                    path = os.path.join(BASE_dir, SUBJECT_DIR, subjectId, assignId)
                    shutil.rmtree(path)
                    assignment.delete()
                    if "deleteLog.txt" in os.listdir(BASE_dir):
                        f = open("deleteLog.txt", "a")
                        f.write(f"In {subjectId} delete {assignId} with user {request.user} time {time}\n")
                        f.close()
                    else:
                        f = open("deleteLog.txt", "w")
                        f.write(f"In {subjectId} delete {assignId} with user {request.user} time {time}\n")
                        f.close()
                    return Response({"result": f'At subject {subjectId} delete assignment {assignId} success.'})
                except OSError as e:
                    return  Response({"error":"This assignment can't delete. please contact admin"})
            except:
                return Response({"error":"suject or assignment doesn't exists"})
        if request.method == 'PUT':
            if 'subjectId' not in request.data:
                return Response({'error': 'Field subjectId not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'assignId' not in request.data:
                return Response({'error': 'Field assignId not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'language' not in request.data:
                return Response({'error': 'Field language not found.'},
                                status=HTTP_400_BAD_REQUEST)
            if 'api' not in request.data:
                api = None
            else: api = request.data['api']

            subjectId = request.data['subjectId'].upper()
            assignId = request.data['assignId'].upper()
            language = request.data['language'].lower()
            if language == 'python':
                language = 'py'

            #set path
            #half path assignment
            path_assignment = os.path.join(SUBJECT_DIR, subjectId, assignId)
            #Full path file
            path_file = os.path.join(BASE_dir, path_assignment)
            #Full path outdated
            path_outdated = os.path.join(path_file, "outdated")
            os.makedirs(path_outdated, exist_ok=True)
            #half path input assignment
            pathIn_save = os.path.join(path_assignment, "input")
            #half path output assignment
            pathOut_save = os.path.join(path_assignment, "output")
            #Full path input assignment
            pathIn = os.path.join(BASE_dir, pathIn_save)
            #Full path output assignment
            pathOut = os.path.join(BASE_dir, pathOut_save)

            #check subject vaild in account
            validSubject = Account.objects.get(user=request.user).idSubject.values_list('idSubject' , flat = True)
            #check assignmrnt vaild in subject
            validAssignment = Assignment.objects.all().filter(idSubject=subjectId).values_list('assignment' , flat = True)
            try:
                assignment = Assignment.objects.get(idSubject=subjectId, assignment=assignId)
                assign_lang = assignment.language
            except:
                pass

            if ('fileAssignment' in request.data):
                fileAssignment = request.FILES['fileAssignment']
                sourceCode = True
            else: sourceCode = False

            status = validError(sourceCode,inOut=False, PUT=True)

            if status['Status']:
                if 'otherFiles' in request.FILES:
                    for file in request.FILES.getlist('otherFiles'):
                        if file and allowed_source_code(file.name):
                            name = secure_filename(file.name)
                            if os.path.exists(os.path.join(path_assignment, name)):
                                newName = time + name
                                shutil.move(os.path.join(path_assignment, name), os.path.join(path_outdated, newName))
                            default_storage.save(os.path.join(path_assignment, name), ContentFile(file.read()))
                        else:
                            return Response({'error': "Other Files isn't Java or Python."},
                                    status=HTTP_400_BAD_REQUEST)
                assignment = Assignment.objects.get(idSubject=subjectId, assignment=assignId)
                filename = assignment.pathMainFile
                if 'fileAssignment' in request.data:
                    filename = secure_filename(fileAssignment.name)
                    typefile = '.' in filename and filename.rsplit('.', 1)[1].lower()
                    if not ((assign_lang == language) and (assign_lang == typefile)):
                        return Response({'Queue':response_code.PROBLEM_STATUS_ERROR_1})
                    storeFileMain()
                    assignment.pathMainFile = filename
                    assignment.save()

                #storage input files
                storeFileInput()

                #storage output files
                storeFileOutput()

                #save data  to database
                data = dictdata()

                #send request to stage2
                res = requests.post(STAGE2, json=data)
                res = json.loads(res.content)
                status['Queue'] = res
            return Response({'Queue': status})
    return Response({"detail":"You do not have permission to access this endpoint. If you need permission please contact admin."})

#URL /finalStage/
@api_view(['POST'])
def api_finalStage(request):
    output = request.body
    data = json.loads(output)
    if not data['data']['api'] is None:
        if(data['status']['boolean']):
            result = {
                "user": data['user'],
                "queue": data['data']['Queue'],
                "Code":data['status']['code'],
                "Description":data['status']['description'],
                "Total Score":data['totalScore'],
                "Result": data['result']
            }
        else:
            result = {
                "user": data['user'],
                "queue": data['data']['Queue'],
                "Code":data['status']['code'],
                "Description":data['status']['description'],
            }
        requests.post(data['data']['api'], json=result)
    if(data['status']['boolean']):
        if data['problem']:
            assignment = Assignment.objects.all().get(id=data['id'])
            assignment.score = data['totalScore']
            pathResult = os.path.join(data['data']['pathAssignment'], 'result.txt')
            file = open(pathResult, "w")
            file.write(json.dumps(data['result'], indent=2))
            file.close()
            assignment.result = pathResult
            assignment.error = False
            assignment.save()
        else:
            user = Score.objects.all().get(id=data['id'])
            user.score = data['totalScore']
            user.check = True
            user.save()
    else:
        if not data['problem']:
            user = Score.objects.all().get(id=data['id'])
            user.error = data['status']['description']
            user.save()
    return Response({'Result': "Success"})