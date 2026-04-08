from django import forms
from .models import InfluencerProfile, Brand, Campaign

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        exclude = ['user', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })
            
            
            

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.FileInput):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
        
        

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['brand', 'created_at']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'deliverables': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.Textarea):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
