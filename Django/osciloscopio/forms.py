from django import forms

class OscilloscopeForm(forms.Form):
    amplitude = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1'
        })
    )
    
    period = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    duration = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1'
        })
    )
    
    frequency = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1'
        })
    )
    
    phase = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.01'
        })
    )