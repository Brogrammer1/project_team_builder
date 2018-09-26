from braces.views import PrefetchRelatedMixin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms


# Create your views here.


class SignUpView(generic.CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('accounts:sign_in')
    template_name = 'accounts/signup.html'


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signin.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, PrefetchRelatedMixin,
                        generic.DetailView):
    model = models.User
    template_name = "accounts/profile.html"
    prefetch_related = ['user_skill_relation', 'projects']

    def get_object(self, queryset=None):
        return self.get_queryset().get(
            pk=self.request.user.pk
        )


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.User
    template_name = 'accounts/addSkills.html'
    form_class = forms.EditProfileForm

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_context_data(self, **kwargs):
        """ gets the modelset and adds it to the context to be rendered"""
        data = super(ProfileEditView, self).get_context_data(**kwargs)
        user_skills = models.UserSkill.objects.filter(
            user=self.request.user)
        if self.request.POST:
            data_post = self.request.POST
            data['skills'] = forms.UserSkillFormSet(data_post, prefix='skills')
        else:
            data['skills'] = forms.UserSkillFormSet(prefix='skills',
                                                    queryset=user_skills)
        return data

    def form_valid(self, form):
        """ creates or updates form instances based on input"""
        context = self.get_context_data()
        skills_form_set = context['skills']
        skills_form_set.is_valid()
        instances = skills_form_set.save(commit=False)
        for instance in instances:
            instance.user = self.object
            instance.save()
        return super(ProfileEditView, self).form_valid(form)
