import json

from _decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from sentence_transformers import util

from employer.forms import JobForm
from employer.models import Job
from employer.forms import QuestionForm
from personality_test.models import Question

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
            personality_1 = form.cleaned_data['personality_1']
            personality_2 = form.cleaned_data['personality_2']
            personality_3 = form.cleaned_data['personality_3']

            job = Job()
            job.title = title
            job.company = company
            job.location = location
            job.summary = summary
            job.description = description
            job.requirements = requirements
            job.start_date = start_date
            job.end_date = end_date
            job.personality_1 = personality_1
            job.personality_2 = personality_2
            job.personality_3 = personality_3

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

def calculate_overall_score(similarity,personality):
    return (personality*100/Decimal(7.5))*Decimal(0.30)+(Decimal(similarity)*Decimal(0.70))

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
            personality_1=form.cleaned_data['personality_1']
            personality_2 = form.cleaned_data['personality_2']
            personality_3 = form.cleaned_data['personality_3']

            job = get_object_or_404(Job, id=id)
            job.title = title
            job.company = company
            job.location = location
            job.summary = summary
            job.description = description
            job.requirements = requirements
            job.start_date = start_date
            job.end_date = end_date
            job.personality_1=personality_1
            job.personality_2=personality_2
            job.personality_3=personality_3

            job.save()

            return redirect('job_list')  # Replace 'login' with the URL name of your login view
    else:

        job = get_object_or_404(Job, id=job_id)
        formatted_start_date = job.start_date.strftime('%Y-%m-%d')
        formatted_end_date = job.end_date.strftime('%Y-%m-%d')

        context = {
            'job': job,
            'formatted_start_date': formatted_start_date,
            'formatted_end_date': formatted_end_date
        }
        return render(request, 'employer/edit-job-detail.html', context)


@login_required(login_url='/login/')
def employer_dashboard(request):
    if request.method == 'GET':
        jobs = Job.objects.annotate(num_applicants=Count('jobapplication'),
                                    num_similarity_check=Count('jobapplication',
                                                               filter=~Q(jobapplication__similarity__isnull=True)))
        return render(request, 'employer/dashboard.html', {'jobs': jobs})


@login_required(login_url='/login')
def analyze(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        jobid = data.get('jobid')

        job = get_object_or_404(Job, id=jobid)
        jobtxt = job.description

        applicants = JobApplication.objects.filter(job__id=jobid)
        resumestxt = []
        for applicant in applicants:
            resumestxt.append(applicant.resume_text)

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        query_embedding = model.encode(jobtxt)
        passage_embedding = model.encode(resumestxt)

        similarity = util.dot_score(query_embedding, passage_embedding)
        print(similarity)
        result = similarity.tolist()
        index = 0
        for applicant in applicants:
            print(result[0][index])
            applicant.similarity = "{:.2f}".format(result[0][index] * 100)
            overall=calculate_overall_score(applicant.similarity,applicant.personality)
            applicant.overall_score=overall
            applicant.save()
            index += 1

        return JsonResponse({"msg": "Resume analysis completed"})


@login_required(login_url='/login')
def analysis_result(request, job_id):
    if request.method == 'GET':
        applicants = JobApplication.objects.filter(job__id=job_id).order_by("-overall_score")
        job = Job.objects.filter(id=job_id)

        return render(request, 'employer/analysis-result.html', {'applicants': applicants, 'job': job[0]})


@login_required(login_url='/login/')
def personality_test_edit(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = QuestionForm()

    questions = Question.objects.all()
    categorized_questions = {}

    for category, _ in Question.CATEGORY_CHOICES:
        categorized_questions[category] = questions.filter(category=category).order_by('id')

    context = {
        'form': form,
        'categorized_questions': categorized_questions,
    }

    return render(request, 'employer/personality_test_edit.html', context)


@login_required(login_url='/login/')
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('personality_test_edit')
