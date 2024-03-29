import time

from _decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q, Case, When, Subquery
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from employer.models import Job
from personality_test.models import UserScore
from .forms import RegisterForm, LoginForm, AccountForm, UploadForm
from .models import CustomUser, JobApplication
import PyPDF2
import boto3
from botocore.exceptions import NoCredentialsError

AWS_ACCESS_KEY_ID = 'AKIARSWFGF3EDTXQKJ66'
AWS_SECRET_ACCESS_KEY = '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'
AWS_BUCKET_NAME = 'cvanalysis-bucket'
AWS_S3_REGION_NAME = 'us-east-2'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_S3_REGION_NAME)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone_number = form.cleaned_data['phone_number']
            if password_confirm == password:
                user = CustomUser()
                user.email = email
                user.password = password
                user.first_name = first_name
                user.last_name = last_name
                user.address = address
                user.city = city
                user.state = state
                user.phone = phone_number
                user.save()

                # Save additional fields to a user profile model if you have one
                # For example, if you have a UserProfile model with the above fields:
                # profile = UserProfile.objects.create(user=user, address=address, city=city, state=state, phone_number=phone_number)

                return redirect('login')  # Replace 'login' with the URL name of your login view
            else:
                form.add_error("password_confirm", "Passwords do not match")

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('employer_dashboard')
                else:
                    login(request, user)
                    return redirect('available_jobs')
            else:
                form.add_error('email', "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='/login/')
def account_view(request):
    user = request.user
    if request.method == 'POST':
        # Handle the form submission for updating user data
        # Retrieve the updated data from the form and update the user object
        # Save the user object
        form = AccountForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone_number = form.cleaned_data['phone_number']

            if password != "":
                user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.city = city
            user.state = state
            user.phone = phone_number
            user.save()
        # Redirect to the "My Account" page or any other desired page
        return redirect('account')

        # Render the template with the user data
    return render(request, 'account.html', {'user': user})


@login_required(login_url='/login/')
def available_job_list(request):
    if request.method == 'GET':
        today = timezone.now().date()
        jobs = Job.objects.filter(end_date__gte=today)

        title_filter = request.GET.get('title', '')
        location_filter = request.GET.get('location', '')
        keywords_filter = request.GET.get('keywords', '')
        if title_filter:
            # If a title filter is provided, apply the filter using Q objects to perform a case-insensitive search
            jobs = jobs.filter(Q(title__icontains=title_filter))
        if location_filter:
            jobs = jobs.filter(Q(location__icontains=location_filter))
        if keywords_filter:
            jobs = jobs.filter(Q(summary__icontains=keywords_filter) or Q(description__icontains=keywords_filter) or Q(
                requirements__icontains=keywords_filter))
        # Annotate the jobs queryset with a BooleanField indicating whether the user has applied for each job
        user = request.user if request.user.is_authenticated else None
        personality_test_score = UserScore.objects.filter(user__id=user.id)

        # Subquery to get a list of job IDs that the user has applied for
        applied_job_ids = JobApplication.objects.filter(user=user).values('job_id')

        # Outer join to get the flag indicating whether the user has applied for the job
        jobs = jobs.annotate(
            applied=Case(
                When(id__in=Subquery(applied_job_ids), then=True),
                default=False,
                output_field=models.BooleanField()
            )
        )
        return render(request, 'job-list.html', {'jobs': jobs, 'personality': (len(personality_test_score))})


@login_required(login_url='/login/')
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user if request.user.is_authenticated else None
    personality_test_score = UserScore.objects.filter(user__id=user.id)
    return render(request, 'job-detail.html', {'job': job, 'personality': (len(personality_test_score))})


def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    print(text)
    return text


def calculate_personality_result(job, personality_test):
    personality = []
    print(job)
    personality.append({job.personality_1: 0.75})
    personality.append({job.personality_2: 0.50})
    personality.append({job.personality_3: 0.25})
    result = 0
    for per in personality:
        personality_trait = list(per.keys())[0]  # Extract the personality trait
        weight = list(per.values())[0]  # Extract the weight
        if personality_trait.lower() == "neuroticism":
            result += personality_test.neuroticism * Decimal(weight)
        elif personality_trait.lower() == "extroversion":
            result += personality_test.extroversion * Decimal(weight)
        elif personality_trait.lower() == "agreeableness":
            result += personality_test.agreeableness * Decimal(weight)
        elif personality_trait.lower() == "conscientiousness":
            result += personality_test.conscientiousness * Decimal(weight)
        elif personality_trait.lower() == "openness":
            result += personality_test.openness * Decimal(weight)
        print(result)
    return "{:.2f}".format(result)


@login_required(login_url='/login/')
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        try:

            text = extract_text_from_pdf(pdf_file)

            job_id = int(request.POST.get('job_id'))
            job = get_object_or_404(Job, id=job_id)
            user_id = request.user.id

            timestamp = int(time.time())
            pdf_filename = f"{timestamp}_{pdf_file.name}"
            with pdf_file.open(mode='rb') as pdf_file_obj:
                s3.upload_fileobj(pdf_file_obj, AWS_BUCKET_NAME, pdf_filename,
                                  ExtraArgs={'ContentType': 'application/pdf'})

            # Construct the S3 URL for the uploaded PDF
            pdf_url = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{pdf_filename}"

            personality_test = get_object_or_404(UserScore, user_id=user_id)
            personality = calculate_personality_result(job, personality_test)
            job_application = JobApplication(job=job, user=request.user, resume_text=text, resume_link=pdf_url,
                                             personality=personality)
            job_application.save()

            return JsonResponse({'message': 'Resume uploaded successfully'})
        except:
            return JsonResponse({'error': 'Resume cannot be uploaded'})

    return render(request, 'job-list.html')
