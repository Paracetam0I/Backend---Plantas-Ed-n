# Plantas Edén — Sitio web en Django

Proyecto de la asignatura **Programación Back End — Evaluación 2**.

Plantas Edén es una pyme chilena (ficticia) que vende plantas de interior y exterior, macetas y semillas de
temporada. El sitio está construido con **Django** a partir de la plantilla **Dopetrope** de HTML5 UP y tiene
cinco secciones, cada una en su propia app. La sección **Blog** es dinámica: sus publicaciones se crean y editan
desde el Panel de Administración de Django y se muestran paginadas (3 por página).

## Requisitos

- Python 3.12 o superior
- Las dependencias de `web-plantas/requirements.txt`: Django 6.1.2 y Pillow 12.3.0 (Pillow es necesario para el
  campo `ImageField`)

## Instalación

Desde la carpeta raíz del repositorio:

```bash
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r web-plantas/requirements.txt
```

La base de datos SQLite (`web-plantas/web_plantas/db.sqlite3`) se entrega con las migraciones aplicadas, el
superusuario y 10 publicaciones de ejemplo. Las imágenes de esas publicaciones están en
`web-plantas/web_plantas/media/blog/`.

## Ejecución

```bash
cd web-plantas/web_plantas
python manage.py runserver
```

Luego abrir <http://127.0.0.1:8000/> en el navegador.

| Sección   | URL         | App       |
|-----------|-------------|-----------|
| Inicio    | `/`         | `core`    |
| Blog      | `/blog/`    | `blog`    |
| Galería   | `/gallery/` | `gallery` |
| Nosotros  | `/about/`   | `about`   |
| Contacto  | `/contact/` | `contact` |
| Panel     | `/admin/`   | —         |

Para ejecutar las pruebas automatizadas:

```bash
python manage.py test
```

## Panel de Administración

- URL: <http://127.0.0.1:8000/admin/>
- Usuario: `root`
- Contraseña: `rootroot`

## Estructura del proyecto

```
web-plantas/
├── requirements.txt
└── web_plantas/               # Carpeta del proyecto (contiene manage.py)
    ├── web_plantas/           # Configuración: settings.py (MEDIA_URL / MEDIA_ROOT) y urls.py
    ├── core/                  # Portada; contiene base.html y los recursos de la plantilla (css, js, fuentes)
    ├── blog/                  # Sección dinámica: modelo Post, admin, vista paginada
    ├── gallery/               # Galería y catálogo de productos
    ├── about/                 # Nosotros y créditos de imágenes
    ├── contact/               # Datos de contacto
    ├── media/blog/            # Imágenes subidas desde el panel
    └── db.sqlite3             # Base de datos SQLite
```

Cada app tiene sus propias carpetas `templates/<app>/` y `static/<app>/`. Todas las páginas heredan de
`core/templates/core/base.html`, que contiene el encabezado, el menú y el pie de página.

En la raíz del repositorio también se conserva la maqueta HTML estática original (`index.html`,
`left-sidebar.html`, `right-sidebar.html`, `no-sidebar.html`, `assets/` e `images/`).

### Modelo `Post` (app `blog`)

| Campo      | Tipo            | Descripción                                                        |
|------------|-----------------|--------------------------------------------------------------------|
| `title`    | `CharField`     | Título de la publicación                                           |
| `subtitle` | `CharField`     | Bajada o subtítulo                                                 |
| `content`  | `TextField`     | Cuerpo del artículo (los párrafos se separan con una línea en blanco) |
| `author`   | `CharField`     | Autor                                                              |
| `category` | `CharField`     | Categoría: interior, exterior, semillas o cuidados                 |
| `image`    | `ImageField`    | Imagen destacada, se guarda en `media/blog/`                       |
| `created`  | `DateTimeField` | Fecha de creación (automática)                                     |
| `updated`  | `DateTimeField` | Fecha de última modificación (automática)                          |

Las publicaciones se ordenan de la más nueva a la más antigua (`ordering = ['-created']`).

## Cómo agregar una publicación al blog

1. Iniciar el servidor y entrar a <http://127.0.0.1:8000/admin/> con `root` / `rootroot`.
2. En **Blog → Publicaciones** presionar **Añadir publicación**.
3. Completar título, subtítulo, contenido, autor y categoría, y elegir una imagen.
4. Presionar **Guardar**. La publicación aparece de inmediato al comienzo de `/blog/`.

Desde el mismo panel se pueden editar o eliminar publicaciones. Las fechas de creación y actualización se
completan solas.

## Créditos

- Diseño basado en la plantilla **Dopetrope** de [HTML5 UP](https://html5up.net), licencia
  [Creative Commons Attribution 3.0](https://html5up.net/license).
- Las fotografías con licencia Creative Commons (CC BY / CC BY-SA) se obtuvieron de Wikimedia Commons. El
  detalle de cada imagen, su autor y su licencia está en la sección **Créditos de imágenes** de la página
  Nosotros (`/about/#creditos`), enlazada también desde el pie de página.

## Integrantes

Ver [`web-plantas/INTEGRANTES.txt`](web-plantas/INTEGRANTES.txt).
