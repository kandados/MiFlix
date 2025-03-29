
from django import forms
from .models import Pelicula, Serie

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí tu título'
            }),
            'sinopsis': forms.Textarea(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full h-32',
                'placeholder': 'Escribe aquí la sinopsis'
            }),
            'estreno': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el año de estreno'
            }),
            'genero': forms.TextInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el género'
            }),
            'director': forms.TextInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el director'
            }),
            'protagonistas': forms.Textarea(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full h-24',
                'placeholder': 'Escribe aquí los protagonistas'
            }),
            'duracion': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí la duración en minutos'
            }),
            'calificacion_usuario': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí la calificación de usuario'
            }),
            'vistas_totales': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el número de vistas'
            }),
            'image_cover': forms.ClearableFileInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
            }),
        }

class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el título de la serie'
            }),
            'sinopsis': forms.Textarea(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full h-32',
                'placeholder': 'Escribe aquí la sinopsis de la serie'
            }),
            'estreno': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el año de estreno'
            }),
            'genero': forms.TextInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el género'
            }),
            'director': forms.TextInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el director'
            }),
            'protagonistas': forms.Textarea(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full h-24',
                'placeholder': 'Escribe aquí los protagonistas'
            }),
            'temporadas_totales': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el número total de temporadas'
            }),
            'capitulos_totales': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el número total de capítulos'
            }),
            'duracion_media_capitulo': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí la duración promedio de los capítulos (en minutos)'
            }),
            'calificacion_usuario': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí la calificación del usuario'
            }),
            'vistas_totales': forms.NumberInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
                'placeholder': 'Escribe aquí el número de vistas totales'
            }),
            'image_cover': forms.ClearableFileInput(attrs={
                'class': 'bg-gray-900 text-white rounded px-4 py-2 w-full',
            }),
        }