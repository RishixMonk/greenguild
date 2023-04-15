from django.shortcuts import render
from api.models import Question
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse, request
# Create your views here.
def questionwithcategory(request,ctg):
    if request.user.is_authenticated:
        try:
            instances = Question.objects.filter(category=ctg)
            data = {'questions': list(instances.values())}
            return JsonResponse(data)
        except:
            return {}
    else:
        return JsonResponse({'error': "User not authenticated"})

def info_of_categories(request):
    if request.user.is_authenticated:
        try:
            instances = Question.objects.values('category').distinct()
            categories = [instance['category'] for instance in instances]
            return JsonResponse({'categories': categories})
        except:
            return {}
    else:
        return JsonResponse({'error': "User not authenticated"})

def submit_data(request):
    if request.user.is_authenticated & request.method == 'POST':
        try:
            form_data = dict(request.POST)
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
                categories[category_data_map[key]]+=question_data_map[key] * float(val[0])
                total_carbon_count+= question_data_map[key] * float(val[0])
            return JsonResponse({'total_carbon_count': total_carbon_count,"categories":categories})
        except Exception as e:
            return JsonResponse({'error': "Key Error"})
    else:
        return JsonResponse({'error': "User not authenticated"})









