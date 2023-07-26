from django.views.generic import ListView
from .pagination import CustomPagination
from .models import Job


class HomeView(ListView):
    template_name = 'core/home.html'  # [[job1, job2], [job3, job4], [job5, job6]]
    pagination_class = CustomPagination
    queryset = Job.objects.filter(is_active=True)

    def get_pagination(self):
        return self.pagination_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Home"
        pagination = self.get_pagination()
        qs = pagination.get_paginated_qs(view=self)  # [job1, job2, job3, job4, job5, job6]
        nested_qs = pagination.get_nested_pagination(qs, nested_size=2)
        context["job_lists"] = nested_qs
        return context
