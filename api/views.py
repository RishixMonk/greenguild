from django.shortcuts import render
from api.models import Question, Score
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse, request
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import math, json
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import urllib.parse
from api.definitions import *
# Create your views here.

def isauth(request):
    # form_data = json.loads(request.body)
    # username = form_data.get("username")
    # password = form_data.get("password")
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username,password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        try:
            instance = Score.objects.get(user=user)
            user_instance = User.objects.get(username=request.user.username)
            return JsonResponse({'username':request.user.username,'carbon_count':instance.carbon_count,'score':instance.score,'date':instance.date,'email':user_instance.email,"status_code":202})
        except ObjectDoesNotExist:
            instance = Score.objects.create(user=user)
            instance.save()
            user_instance = User.objects.get(username=request.user.username)
            return JsonResponse({'username':request.user.username,'carbon_count':instance.carbon_count,'score':instance.score,'email':user_instance.email,"status_code":202})
    else:
        return JsonResponse({'error': "User not authenticated","status_code":203})

def register_request(request):
    if request.method == "POST":
        userName = request.POST.get('username', None)
        try:
            instance = User.objects.get(username=userName)
            return JsonResponse({'msg':"Username Already Exists", 'status_code':203})
        except ObjectDoesNotExist:
            userPass = request.POST.get('password', None)
            userMail = request.POST.get('email', None)
            user = User.objects.create_user(userName, userMail, userPass)
            user.save()
            login(request, user)
            instance = Score.objects.create(user=user)
            user_instance = User.objects.get(username=request.user.username)
            return JsonResponse({'username':request.user.username,'carbon_count':instance.carbon_count,'score':instance.score,'date':instance.date,'email':user_instance.email,"status_code":202})
    return JsonResponse({'status':"Unsuccessful registration. Invalid information.","status_code":203})

def questionwithcategory(request,ctg):
    # if request.user.is_authenticated:
    try:
        instances = Question.objects.filter(category=ctg)
        data = {'questions': list(instances.values())}
        return JsonResponse(data)
    except:
        return {}
    # else:
    #     return JsonResponse({'error': "User not authenticated"})

def info_of_categories(request):
    # if request.user.is_authenticated:
    print("code yahan taka aaya")
    try:
        print('try')
        instances = Question.objects.values('category').distinct()
        categories = [instance['category'] for instance in instances]
        return JsonResponse({'categories': categories})
    except:
        print('except')
        return {}
    # else:
    #     return JsonResponse({'error': "User not authenticated"})

def submit_data(request):
    # if request.user.is_authenticated and request.method == 'POST':
    if request.method == 'POST':
        try:
            url_encoded_data = request.body
            decoded_data = urllib.parse.unquote(url_encoded_data.decode())
            decoded_data = decoded_data.split("&")
            print(decoded_data)
            form_data = json.loads(decoded_data[0].split("=")[1])
            username = decoded_data[1].split("=")[1]
            question_data_map = {}
            category_data_map = {}
            TOTAL = AVG_CONSUMPTION_COMMUTE + AVG_CONSUMPTION_HOUSEHOLD + AVG_CONSUMPTION_FOOD
            instances = list(Question.objects.all())
            categories_db = Question.objects.values('category').distinct()
            categories = {str(instance['category']):0 for instance in categories_db}
            for question in instances:
                question_data_map[str(question.id)] = question.value
                category_data_map[str(question.id)] = question.category
            total_carbon_count = 0
            for key, val in form_data.items():
                categories[category_data_map[key]]+=question_data_map[key] * float(val)
                total_carbon_count+= question_data_map[key] * float(val)
            total_score = -int((total_carbon_count-TOTAL)/10)
            commute_score = -int((categories['Commute']-AVG_CONSUMPTION_COMMUTE)/10)
            household_score = -int((categories['Household']-AVG_CONSUMPTION_HOUSEHOLD)/10)
            food_score = int(categories['Food']/10)
            scores = {
                "total_score": math.floor(total_score),
                "commute_score": math.floor(commute_score),
                "household_score": math.floor(household_score),
                "food_score": math.floor(total_score) - (math.floor(commute_score) + math.floor(household_score))
            }
            instance = Score.objects.get(user=User.objects.get(username=username))
            instance.score += total_score
            instance.carbon_count = round(total_carbon_count,2)
            instance.date = datetime.now()
            instance.save()
            return JsonResponse({'total_carbon_count': total_carbon_count,"categories":categories,"scores":scores})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': "User not authenticated"})
    

def leaderboard(request):
    if request.user.is_authenticated:
        try:
            instances = Score.objects.all().order_by('-score')
            data = {'leaderboard': list(instances.values())}
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error':str(e)})
    else:
            return JsonResponse({'error': "User not authenticated"})
    

def logout_view(request):
    print(request.user.username)
    logout(request)
    return JsonResponse({'msg': "Logged Out"})











