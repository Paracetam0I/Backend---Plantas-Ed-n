from django import forms

# Formulario de contacto.
# Es un forms.Form y no un ModelForm: no se guarda nada en la BD, por eso la app no tiene modelos.
class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre", required=True, min_length=3, max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': "Escribe aquí tu nombre",
                                                         'class': 'form-control'}))
    email = forms.EmailField(label="Email", required=True, min_length=3, max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': "Escribe aquí tu correo",
                                                           'class': 'form-control'}))
    content = forms.CharField(label="Mensaje", required=True, min_length=10, max_length=500,
                              widget=forms.Textarea(attrs={'placeholder': "Escribe aquí tu Mensaje",
                                                           'rows': 3, 'class': 'form-control'}))
