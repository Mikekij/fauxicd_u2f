from django import forms
from web.models import Icd

class IcdForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="ICD Name:")
    zap_duration = forms.IntegerField(help_text="Milliseconds to Execute Shock:")
    keys_required = forms.IntegerField(help_text="Number of Keys Required to Shock:")

    class Meta:
        model = Icd

        #fields = ('name', 'zap_duration', 'keys_required',)
