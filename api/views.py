from django.shortcuts import render
from api.models import Question
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse
# Create your views here.
def questionwithcategory(request,ctg):
    try:
        instances = Question.objects.filter(category=ctg)
        data = {'questions': list(instances.values())}
        return JsonResponse(data)
    except:
        return {}

def info_of_categories(request):
    instances = Question.objects.values('category').distinct()
    categories = [instance['category'] for instance in instances]
    return JsonResponse({'categories': categories})








