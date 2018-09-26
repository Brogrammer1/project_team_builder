from braces.views import PrefetchRelatedMixin, SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from . import forms
from . import models


class AllProjects(LoginRequiredMixin, PrefetchRelatedMixin, generic.ListView):
    model = models.Project
    prefetch_related = ["positions"]
    template_name = 'index.html'

    def get_queryset(self):
        """returns different querysets based on get received"""
        if self.request.GET.get('q'):
            return models.Project.objects.filter(
                title__icontains=self.request.GET.get('q')
            )
        elif self.request.GET.get('filter'):
            return models.Project.objects.filter(
                positions__title__icontains=self.request.GET.get('filter')
            )
        else:
            return models.Project.objects.all()


class ProjectDetailView(LoginRequiredMixin, PrefetchRelatedMixin,
                        generic.DetailView):
    model = models.Project
    prefetch_related = ["positions"]
    template_name = 'projects/project.html'


class CreateProjectPositionView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProjectForm
    model = models.Project
    template_name = 'projects/project_new.html'

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """ adds formset to the context data"""
        data = super(CreateProjectPositionView, self).get_context_data(
            **kwargs)
        if self.request.POST:
            data_post = self.request.POST
            data['positions'] = forms.PositionFormSet(data_post,
                                                      prefix='positions')
        else:
            data['positions'] = forms.PositionFormSet(prefix='positions')
        return data

    def form_valid(self, form):
        """ checks if data is valid then sets missing fields of each object
        then saves to database"""
        context = self.get_context_data()
        positions_form_set = context['positions']

        if form.is_valid() and positions_form_set.is_valid():
            self.object = form.save(commit=False)
            self.object.creator = self.request.user
            self.object.save()

            for position_form in positions_form_set:
                if (position_form.cleaned_data.get('skill') and
                        position_form.cleaned_data.get('title')):
                    position_obj = position_form.save(commit=False)
                    position_obj.project = self.object
                    position_obj.save()
        return super(CreateProjectPositionView, self).form_valid(form)


class TestEditView(LoginRequiredMixin, generic.CreateView, generic.UpdateView):
    form_class = forms.ProjectForm
    model = models.Project
    template_name = "projects/project_edit.html"

    def get_success_url(self):
        return reverse_lazy('projects:detail',
                            kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super(TestEditView, self).get_context_data(**kwargs)
        user_skills = models.Position.objects.filter(
            project=self.object)
        if self.request.POST:
            data_post = self.request.POST
            data['positions'] = forms.test(data_post, prefix='positions')
        else:
            data['positions'] = forms.test(prefix='positions',
                                           queryset=user_skills)
        return data

    def form_valid(self, form):
        """checks if data is valid then updates or creates new instances"""
        context = self.get_context_data()
        positions_form_set = context['positions']
        positions_form_set.is_valid()
        instances = positions_form_set.save(commit=False)
        for instance in instances:
            instance.project = self.object
            instance.save()
        return super(TestEditView, self).form_valid(form)


class CreateApplicationView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:detail', kwargs={'pk': self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        """gets the position then checks if a previous application for the
        position already exists, if not it creates a new application"""
        try:
            position = models.Position.objects.get(
                pk=self.kwargs['position_pk'])
        except models.Position.DoesNotExist:
            messages.warning(
                self.request,
                "You can't apply to this position."
            )
        else:
            try:
                previous_application = models.Application.objects.get(
                    position=position,
                    candidate=self.request.user)
            except models.Application.DoesNotExist:
                models.Application.objects.create(
                    position=position,
                    candidate=self.request.user)
                messages.success(self.request, "You have applied to the {}"
                                               " position".format(
                    position.title))

            else:
                messages.warning(
                    self.request,
                    "You can't apply to the same position twice"
                )
        return super().get(request, *args, **kwargs)


class AllApplications(LoginRequiredMixin, PrefetchRelatedMixin,
                      generic.ListView):
    model = models.Application
    prefetch_related = ["candidate", "position"]
    template_name = 'projects/applications.html'

    def get_context_data(self, *args, **kwargs):
        """adds the projects created by the user to the context"""
        context = super(AllApplications, self).get_context_data(*args,
                                                                **kwargs)
        context['projects'] = models.Project.objects.filter(
            creator=self.request.user)
        return context

    def get_queryset(self):
        """gets the queryset based on get kwargs passed in
        to filter the results """
        apps = models.Application.objects.filter(
            position__project__creator=self.request.user
        )

        if self.request.GET.get('pk'):
            apps = apps.filter(
                position__project__pk=self.request.GET.get('pk')
            )
        elif self.request.GET.get('status'):
            apps = apps.filter(
                status=self.request.GET.get('status')
            )

        elif self.request.GET.get('filter'):
            apps = apps.filter(
                position__title__icontains=self.request.GET.get('filter')
            )
        else:
            apps = apps.filter(
                status='processing'
            )


        return apps


class ApplicationsDetailView(LoginRequiredMixin, SelectRelatedMixin,
                             generic.DetailView):
    model = models.Application
    select_related = ["candidate"]


class AcceptRejectApplicationView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy('projects:applications')

    def get_object(self):
        return get_object_or_404(models.Application, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        """ sets the application status field to the kwarg received .
        sends thr applicant a email of the decision made
         then redirects back to the applications"""
        application = self.get_object()

        decision = self.kwargs.get('decision')
        application.status = decision
        if decision == 'Accepted':
            application.position.filled = True
            application.position.save()

        application.save()
        send_mail(
            '{} application'.format(application.position.title),
            'Your application has been {}'.format(decision),
            'ProjectBuilder.com',
            [application.candidate.email],
            fail_silently=False,
        )

        return super().get(request, *args, **kwargs)


class DeleteProjectView(LoginRequiredMixin, generic.DeleteView):
    model = models.Project
    template_name = 'projects/delete_project.html'
    success_url = reverse_lazy('projects:all_projects')

    def delete(self, *args, **kwargs):
        """deletes the project notifies user of such action """
        messages.success(self.request, "You have Successfully deleted"
                                       " a project")
        return super().delete(*args, **kwargs)
