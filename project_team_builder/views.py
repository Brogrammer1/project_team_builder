from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView

# Create your views here.
from projects import models


class Home(ListView):
    template_name = 'search.html'
    model = models.Project

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("projects:all_projects"))
        return super().get(request, *args, **kwargs)
