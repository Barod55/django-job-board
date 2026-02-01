from urllib import request
from django.shortcuts import render
from django.urls import reverse
from job import form
from .models import Job
from django.core.paginator import Paginator
from .form import ApplyForm , JobForm 
from django.shortcuts import redirect

# Create your views here.

def job_list(request):
  job_list = Job.objects.all()
  paginator = Paginator(job_list, 4)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  # Show 10 jobs per page
  context = {'jobs': page_obj}
  return render(request, 'job/job_list.html', context)

def job_detail(request,slug):
  job_detail = Job.objects.get(slug=slug)
  
  if request.method == 'POST':
      form = ApplyForm(request.POST , request.FILES)
      if form.is_valid():
          apply = form.save(commit=False)
          apply.job = job_detail
          apply.save()
      else:
          print(form.errors)
  else:
      form = ApplyForm()
  
  context = {'job': job_detail, 'form': form}
  return render(request, 'job/job_detail.html', context)

def add_job(request):
  if request.method == 'POST':
      form = JobForm(request.POST , request.FILES)
      if form.is_valid():
          myform = form.save(commit=False)
          myform.owner = request.user
          myform.save()
          return redirect(reverse('job:job_list'))
      else:
          print(form.errors)
  return render(request, 'job/add_job.html',{'form': JobForm})
