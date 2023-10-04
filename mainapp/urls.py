from django.urls import path,include
from .views import PetroleumDataView,DisplayPetroleumDataView
app_name = "mainapp"
urlpatterns = [
    path('petroleum-data/',PetroleumDataView.as_view(), name="show"),
    path('display-petroleum-data/', DisplayPetroleumDataView.as_view(), name="display-petroleum-data"),
    
]
