from django import forms
from .models import Team, Match
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'manager']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'home_score', 'away_score', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        # Set default value to today if not already set
        if not self.initial.get('date'):
            self.initial['date'] = datetime.date.today()
