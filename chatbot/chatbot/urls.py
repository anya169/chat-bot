from django.contrib import admin
from django.urls import path, re_path
from adminsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'young_employees/$', views.young_employee_list),
]
