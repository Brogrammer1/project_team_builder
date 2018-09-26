from django import forms
from django.forms import inlineformset_factory
from accounts.models import Skill
from . import models


class ProjectForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'circle--input--h1',
               'placeholder': 'Project Title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'project description...'}))
    time_line_description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'circle--textarea--input',
               'placeholder': 'Time estimate'}))

    class Meta:
        model = models.Project
        fields = (
            'title',
            'description',
            'time_line_description',
            'applicant_req'
        )


class PositionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'position description...'}
    )
    )
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        empty_label='Select related skill')
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'position name...'}))

    class Meta:
        model = models.Position
        fields = (
            'title',
            'skill',
            'description',
        )


PositionFormSet = inlineformset_factory(models.Project,
                                        models.Position,
                                        form=PositionForm,
                                        extra=5, min_num=0,
                                        can_delete=True)

test = forms.modelformset_factory(models.Position,
                                  form=PositionForm,
                                  extra=2,
                                  can_delete=True)
