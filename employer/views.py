import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from sentence_transformers import util

from employer.forms import JobForm
from employer.models import Job
from users.models import JobApplication
from sentence_transformers import SentenceTransformer

@login_required(login_url='/login/')
def employer_dashboard(request):
    return render(request, 'employer/dashboard.html')


@login_required(login_url='/login/')
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            company = form.cleaned_data['company']
            location = form.cleaned_data['location']
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']
            requirements = form.cleaned_data['requirements']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            job = Job()
            job.title = title
            job.company = company
            job.location = location
            job.summary = summary
            job.description = description
            job.requirements = requirements
            job.start_date = start_date
            job.end_date = end_date

            job.save()

            return redirect('create_job')  # Replace 'login' with the URL name of your login view
    else:
        form = JobForm()

    return render(request, 'employer/create-job.html', {'form': form})


def job_list(request):
    if request.method == 'GET':
        today = timezone.now().date()
        jobs = Job.objects.filter(end_date__gte=today)
        expired_jobs = Job.objects.filter(end_date__lt=today)
        return render(request, 'employer/job-list.html', {'jobs': jobs, "expired_jobs": expired_jobs})


@login_required(login_url='/login/')
def edit_job_detail(request, job_id):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            title = form.cleaned_data['title']
            company = form.cleaned_data['company']
            location = form.cleaned_data['location']
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']
            requirements = form.cleaned_data['requirements']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            job = get_object_or_404(Job, id=id)
            job.title = title
            job.company = company
            job.location = location
            job.summary = summary
            job.description = description
            job.requirements = requirements
            job.start_date = start_date
            job.end_date = end_date

            job.save()

            return redirect('job_list')  # Replace 'login' with the URL name of your login view
    else:

        job = get_object_or_404(Job, id=job_id)

        context = {
            'job': job
        }
        return render(request, 'employer/edit-job-detail.html', context)


@login_required(login_url='/login/')
def employer_dashboard(request):
    if request.method == 'GET':
        jobs = Job.objects.annotate(num_applicants=Count('jobapplication'))
        return render(request, 'employer/dashboard.html', {'jobs': jobs})

@login_required(login_url='/login')
def analyze(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        jobid = data.get('jobid')

        job = get_object_or_404(Job, id=jobid)
        jobtxt =job.description

        applicants=JobApplication.objects.filter(job__id=jobid)
        resumestxt=[]
        for applicant in applicants:
            resumestxt.append(applicant.resume_text)

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        query_embedding = model.encode(jobtxt)
        passage_embedding = model.encode(resumestxt)

        similarity=util.dot_score(query_embedding, passage_embedding)

        result=similarity.tolist()
        index=0
        for applicant in applicants:
            print(result[index][0])
            applicant.similarity=result[index][0]
            applicant.save()

        return render(request, 'employer/dashboard.html')