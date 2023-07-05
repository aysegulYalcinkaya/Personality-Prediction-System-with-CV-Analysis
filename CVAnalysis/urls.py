"""
URL configuration for CVAnalysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import register, dashboard, account_view, available_job_list
from users.views import login_view
from employer.views import employer_dashboard, create_job, job_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('job-list/', available_job_list, name='available_jobs'),
    path('', login_view, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('account/', account_view, name='account'),
    path('logout/', LogoutView.as_view(next_page='/dashboard'), name='logout'),
    path('employer/dashboard/', employer_dashboard, name='employer_dashboard'),
    path('employer/create-job/', create_job, name='create_job'),
    path('employer/job-list/', job_list, name='job_list')
]
