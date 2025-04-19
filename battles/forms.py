# battles/forms.py
from django import forms
from .models import Battle
from django.utils import timezone

class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['battle_type', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if start_time < timezone.now():
                raise forms.ValidationError("Döyüş gələcək bir vaxt üçün planlaşdırılmalıdır!")
            if end_time <= start_time:
                raise forms.ValidationError("Bitmə vaxtı başlama vaxtından sonra olmalıdır!")
        
        return cleaned_data