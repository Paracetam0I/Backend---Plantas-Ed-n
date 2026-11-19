from .models import BusinessInfo


# Procesador de contexto: función que recibe el request y devuelve un diccionario.
# Está registrada en settings.py (TEMPLATES -> context_processors), por eso Django la ejecuta en cada
# render() y agrega su diccionario al contexto de TODAS las plantillas, de cualquier app.
# Sin registrarla, {{ INFO_CORREO }} quedaría vacío (Django no marca error, solo no imprime nada).
def ctx_dict(request):
    ctx = {}
    infos = BusinessInfo.objects.all()
    # Cada dato se agrega con su clave como nombre: ctx['INFO_CORREO'] = 'contacto@plantaseden.cl'
    for info in infos:
        ctx[info.key] = info.value
    return ctx
