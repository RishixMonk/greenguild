from django.urls import path,include
from api import views

urlpatterns = [
    path('qtc/<ctg>', views.questionwithcategory),
    path('all',views.info_of_categories),
    path('submit',views.submit_data),
    path('isauth',views.isauth),
    path('register_request',views.register_request),
    path('leaderboard',views.leaderboard),
    path('logout',views.logout_view),
]

