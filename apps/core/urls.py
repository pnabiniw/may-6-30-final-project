from django.urls import path
from .views import HomeView, JobDetailView, job_apply, MyJobsView, ContactView


urlpatterns = [
    path('job-detail/<str:uuid>/', JobDetailView.as_view(), name='job_detail'),
    path('job-apply/<str:uuid>/', job_apply, name='job_apply'),
    path('my-jobs/', MyJobsView.as_view(), name='my_jobs'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('', HomeView.as_view(), name='home')
]
