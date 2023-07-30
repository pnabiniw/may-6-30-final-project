from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import redirect
from apps.commons.utils import get_base_url, is_profile_complete
from .pagination import CustomPagination
from .models import Job, Category, JobApplication
from .forms import ContactForm


class HomeView(ListView):
    template_name = 'core/home.html'  # [[job1, job2], [job3, job4], [job5, job6]]
    pagination_class = CustomPagination

    def get_pagination(self):
        return self.pagination_class()

    def get_queryset(self):
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        job_filter = {"is_active": True}
        exclude = dict()
        if self.request.user.is_authenticated:
            exclude = {"job_applications__user": self.request.user}
        if category:
            job_filter.update(category__uuid=category)
        if search:
            job_filter.update(title__icontains=search)
        return Job.objects.filter(**job_filter).exclude(**exclude).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        pagination = self.get_pagination()
        qs = pagination.get_paginated_qs(view=self)
        paginated_qs = pagination.get_nested_pagination(qs, nested_size=2)
        context['job_lists'] = paginated_qs
        context['categories'] = Category.objects.all()
        page_number, page_str = pagination.get_current_page(view=self)
        context[page_str] = 'active'
        context["next_page"] = page_number + 1
        context["prev_page"] = page_number - 1
        context['base_url'] = get_base_url(request=self.request)
        if page_number >= pagination.get_last_page(view=self):
            context["next"] = "disabled"
        if page_number <= 1:
            context["prev"] = "disabled"
        context['home_active'] = 'active'
        return context


class JobDetailView(DetailView):
    template_name = 'core/job_detail.html'
    queryset = Job.objects.filter(is_active=True)
    slug_field = 'uuid'  # This must be a unique field from the table
    slug_url_kwarg = 'uuid'  # This must be exactly from the url
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Job Detail"
        return context


@login_required
def job_apply(request, uuid):
    try:
        job = Job.objects.get(uuid=uuid)
    except Job.DoesNotExist:
        messages.error(request, "Something Went Wrong!!")
        return redirect('home')
    if is_profile_complete(request.user):  # Apply for Job
        JobApplication.objects.get_or_create(user=request.user, job=job, defaults={"status": "APPLIED"})
        messages.success(request, f"You Have Successfully Applied For The Role Of {job.title}")
        return redirect('home')
    messages.error(request, "Please Activate Your Account And Complete Your Profile !!")
    return redirect('home')


@method_decorator(login_required, name='dispatch')
class MyJobsView(ListView):
    template_name = 'core/my_jobs.html'
    context_object_name = 'job_applications'

    def get_queryset(self):
        status = self.request.GET.get("status")
        filter_dict = dict(user=self.request.user)
        if status:
            filter_dict.update(status=status)
        return JobApplication.objects.filter(**filter_dict)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = ["APPLIED", "SCREENING", "SHORT_LISTED", "REJECTED", "SELECTED"]
        context["my_jobs_active"] = 'active'
        return context


class ContactView(CreateView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "We Have Received Your Response")
            return self.form_valid(form)
        else:
            messages.error(request, "Something Went Wrong")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Contact Us"
        context['contact_active'] = 'active'
        return context
