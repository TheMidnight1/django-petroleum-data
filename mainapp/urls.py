from django.urls import path,include
from .views import DisplayPetroleumDataView
app_name = "mainapp"
urlpatterns = [
    path('', DisplayPetroleumDataView.as_view(), name="display-petroleum-data"),
    
]
