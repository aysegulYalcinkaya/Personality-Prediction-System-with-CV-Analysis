from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from employer.forms import JobForm
from employer.models import Job


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
