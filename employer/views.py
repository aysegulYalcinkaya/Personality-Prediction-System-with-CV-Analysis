from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
            job.title=title
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

    return render(request, 'employer/create-job.html',{'form': form})

@login_required(login_url='/login/')
def job_list(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        return render(request, 'employer/job-list.html', {'jobs': jobs})