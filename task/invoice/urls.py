from django.urls import path

from .views import ItemViewSet, GeneratePdf

urlpatterns = [
    path('api/item_add/', ItemViewSet.as_view()),  
    path('pdf/<id>/', GeneratePdf.as_view()) ,
]
