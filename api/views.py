from django.shortcuts import render
from api.models import Question
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse, request
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import math, json
# Create your views here.

def isauth(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username,password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': "User authenticated"})
    else:
        return JsonResponse({'error': "User not authenticated"})

def register_request(request):
    if request.method == "POST":
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password', None)
        userMail = request.POST.get('email', None)
        user = User.objects.create_user(userName, userMail, userPass)
        user.save()
        login(request, user)
        return JsonResponse({'status': "Registration successful"})
    return JsonResponse({'status':"Unsuccessful registration. Invalid information."})

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
    try:
        instances = Question.objects.values('category').distinct()
        categories = [instance['category'] for instance in instances]
        return JsonResponse({'categories': categories})
    except:
        return {}
    # else:
    #     return JsonResponse({'error': "User not authenticated"})

def submit_data(request):
    # if request.user.is_authenticated and request.method == 'POST':
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body)
            question_data_map = {}
            category_data_map = {}
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
            total_score = int(total_carbon_count/10)
            commute_score = int(categories['Commute']/10)
            household_score = int(categories['Household']/10)
            food_score = int(categories['Food']/10)
            scores = {
                "total_score": math.floor(total_score),
                "commute_score": math.floor(commute_score),
                "household_score": math.floor(household_score),
                "food_score": math.floor(total_score) - (math.floor(commute_score) + math.floor(household_score))
            }
            return JsonResponse({'total_carbon_count': total_carbon_count,"categories":categories,"scores":scores})
        except Exception as e:
            return JsonResponse({'error': "Key Error"})
    else:
        return JsonResponse({'error': "User not authenticated"})









