from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job
from .form import ApplyForm, JobForm
from .filters import JobFilter

# Number of jobs per page (change as needed)
JOBS_PER_PAGE = 4


def job_list(request):
    job_list = Job.objects.all()
    ##filter 
    myfilter = JobFilter(request.GET, queryset=job_list)
    job_list = myfilter.qs
    jobs = job_list.select_related('owner', 'category').order_by('-published_at')
    paginator = Paginator(jobs, JOBS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'jobs': page_obj, 'myfilter': myfilter}
    return render(request, 'job/job_list.html', context)


def job_detail(request, slug):
    """Show job details and handle application submissions.

    Uses get_object_or_404 and implements a Post/Redirect/Get flow with messages.
    """
    job = get_object_or_404(Job, slug=slug)

    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            apply = form.save(commit=False)
            apply.job = job
            apply.save()
            messages.success(request, 'Your application has been submitted.')
            return redirect(reverse('job:job_detail', kwargs={'slug': job.slug}))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplyForm()

    context = {'job': job, 'form': form}
    return render(request, 'job/job_detail.html', context)


@login_required
def add_job(request):
    """Allow authenticated users to create a new job posting.

    Requires login and uses messages for feedback.
    """
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('job:job_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()

    return render(request, 'job/add_job.html', {'form': form})
