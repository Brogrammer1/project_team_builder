from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from . import models


class UserCreationForm(UserCreationForm):
    class Meta:
        fields = ('email', 'password1', 'password2',)
        model = get_user_model()


class EditProfileForm(forms.ModelForm):
    bio = forms.Textarea()
    display_name = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('display_name',
                  'bio',
                  'avatar',)


class UserSkillForm(forms.ModelForm):
    class Meta:
        fields = ('skill',)
        model = models.UserSkill


UserSkillFormSet = forms.modelformset_factory(models.UserSkill,
                                              form=UserSkillForm,
                                              extra=5, min_num=0, max_num=5)

