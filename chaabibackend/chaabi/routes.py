from django.urls import re_path, path
from chaabi.Views.ChaabiView import *

urlpatterns = [

    re_path(r'health/check/v(?P<version_id>\d+)/', HealthCheckView.as_view()),
    
]