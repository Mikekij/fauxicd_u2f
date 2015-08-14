from django import forms
from django.contrib.auth.models import User
from web.models import Icd, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('icd_id',)


class IcdForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="ICD Name:")
    zap_duration = forms.IntegerField(help_text="Milliseconds to Execute Shock:")
    keys_required = forms.IntegerField(help_text="Number of Keys Required to Shock:")

    class Meta:
        model = Icd
        fields = ('name', 'zap_duration', 'keys_required',)
