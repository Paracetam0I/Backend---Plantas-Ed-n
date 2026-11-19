from django.db import models


# Modelo BusinessInfo: datos del negocio que se repiten en varias páginas (dirección, correo, teléfono, horario).
# Cada fila es un par clave/valor; processors.py los entrega a TODAS las plantillas.
# Así se editan una sola vez en el Panel de Django y cambian en el footer, Contacto y Tienda a la vez.
class BusinessInfo(models.Model):
    # SlugField: texto sin espacios (letras, números, _ y -). Es el nombre de la variable en las plantillas,
    # ej. INFO_CORREO -> {{ INFO_CORREO }}. unique=True impide dos datos con la misma clave.
    key = models.SlugField(verbose_name="Nombre clave", max_length=100, unique=True)
    # Nombre legible para identificar el dato en el panel (ej. "Correo de contacto")
    name = models.CharField(verbose_name="Dato", max_length=100)
    # TextField para admitir textos largos; null/blank permiten dejarlo vacío (la plantilla no lo muestra)
    value = models.TextField(verbose_name="Valor", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Dato del negocio"
        verbose_name_plural = "Datos del negocio"
        ordering = ['name']

    def __str__(self):
        return self.name
