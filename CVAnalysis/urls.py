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

from personality_test.views import personality_test
from users.views import register, dashboard, account_view, available_job_list, upload_pdf, job_detail
from users.views import login_view
from employer.views import employer_dashboard, create_job, job_list, edit_job_detail, personality_test_edit, \
    delete_question, analyze

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('job-list/', available_job_list, name='available_jobs'),
    path('job-detail/<int:job_id>/',job_detail,name='job_detail'),
    path('', login_view, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('account/', account_view, name='account'),
    path('logout/', LogoutView.as_view(next_page='/dashboard'), name='logout'),
    path('employer/dashboard/', employer_dashboard, name='employer_dashboard'),
    path('employer/create-job/', create_job, name='create_job'),
    path('employer/job-list/', job_list, name='job_list'),
    path('employer/edit-job-detail/<int:job_id>/',edit_job_detail,name='edit_job_detail'),
    path('upload_pdf', upload_pdf, name='upload_pdf'),
    path('personality_test/', personality_test, name='personality_test'),
    path('personality_test_edit/', personality_test_edit, name='personality_test_edit'),
    path('employer/delete_question/<int:question_id>/', delete_question, name='delete_question'),
    path('employer/analyze', analyze, name='analyze')
]
