from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    # dennis ivy
    path('', views.getDataFromManageClassTable,
         name='getDataFromManageClassTable'),
    path('post-class', views.postDataToManageClassTable,
         name='postDataToManageClassTable'),


    #     not dennis  ivy
    path('modify-class<str:id>/', views.getOrPutOrDeleteDataFromManageClassTable)
]
