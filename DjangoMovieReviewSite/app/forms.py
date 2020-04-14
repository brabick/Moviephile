"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import tbl_movie_scores

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
        
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]

class tbl_movie_scores_form(ModelForm):
    class Meta:
        model = tbl_movie_scores
        fields = [
            'sound', 'cinematography', 'story_telling', 'acting', 'plausibility',
            'cast', 'effects', 'fun_factor', 'originality', 'characters', 'review'
            ]