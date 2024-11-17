# ClonFlixApp/forms.py
from django import forms

class CalificacionForm(forms.Form):
    calificacion = forms.DecimalField(max_digits=3, decimal_places=1, min_value=0, max_value=10, required=True)
