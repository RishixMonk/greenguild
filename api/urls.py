from django.urls import path,include
from api import views

urlpatterns = [
    path('qtc/<ctg>', views.questionwithcategory),
    path('all/',views.info_of_categories)
]

