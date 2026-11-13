# Plantas Edén — Sitio web en Django

Proyecto de la asignatura **Programación Back End — Evaluaciones 2 y 3**.

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
| Categoría | `/category/<id>/` | `blog` |
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
    ├── blog/                  # Sección dinámica: modelos Post, Category y Author, admin, vistas blog y category
    ├── info/                  # Datos del negocio + processors.py (contenido global para todas las plantillas)
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

### Modelos relacionados (app `blog`)

```
Author 1 ──── N Post N ──── N Category
       (ForeignKey)   (ManyToManyField)
```

**`Post`**

| Campo        | Tipo                        | Descripción                                                        |
|--------------|-----------------------------|--------------------------------------------------------------------|
| `title`      | `CharField`                 | Título de la publicación                                           |
| `subtitle`   | `CharField`                 | Bajada o subtítulo                                                 |
| `content`    | `TextField`                 | Cuerpo del artículo (los párrafos se separan con una línea en blanco) |
| `author`     | `ForeignKey(Author)`        | Autor de la publicación                                            |
| `categories` | `ManyToManyField(Category)` | Una o más categorías                                               |
| `image`      | `ImageField`                | Imagen destacada, se guarda en `media/blog/`                       |
| `published`  | `DateTimeField`             | Fecha de publicación (por defecto, el momento de crearla; editable) |
| `created`    | `DateTimeField`             | Fecha de creación (automática)                                     |
| `updated`    | `DateTimeField`             | Fecha de última modificación (automática)                          |

Las publicaciones se ordenan de la más nueva a la más antigua (`ordering = ['-published']`).

**`Category`**: `name`, `created`, `updated`. Desde una categoría se obtienen sus posts con `category.post_set.all`.

**`Author`**: `name`, `specialty`, `photo` (opcional, se guarda en `media/authors/`), `created`, `updated`.

### Datos del negocio (app `info`)

El modelo `BusinessInfo` guarda pares clave/valor (`key`, `name`, `value`, `created`, `updated`). La función
`ctx_dict` de `info/processors.py` está registrada en `TEMPLATES → context_processors` de `settings.py` y agrega
cada dato al contexto de **todas** las plantillas, sin que las vistas lo envíen. Se usan en el pie de página,
en Contacto y en Tienda:

| Clave                  | Dato                       |
|------------------------|----------------------------|
| `INFO_DIRECCION`       | Dirección                  |
| `INFO_CORREO`          | Correo de contacto         |
| `INFO_CORREO_EVENTOS`  | Correo de eventos          |
| `INFO_TELEFONO`        | Teléfono de la tienda      |
| `INFO_WHATSAPP`        | WhatsApp                   |
| `INFO_HORARIO_SEMANA`  | Horario lunes a viernes    |
| `INFO_HORARIO_SABADO`  | Horario sábado             |
| `INFO_HORARIO_DOMINGO` | Horario domingo y festivos |

Si se cambia un valor en **Información del negocio → Datos del negocio**, cambia en todo el sitio a la vez.

## Cómo agregar una publicación al blog

1. Iniciar el servidor y entrar a <http://127.0.0.1:8000/admin/> con `root` / `rootroot`.
2. En **Blog → Publicaciones** presionar **Añadir publicación**.
3. Completar título, subtítulo y contenido, elegir el autor (o crearlo con **+**), pasar una o más categorías a
   la caja de la derecha y elegir una imagen.
4. Presionar **Guardar**. La publicación aparece al comienzo de `/blog/` y en la página de cada una de sus
   categorías.

Desde el mismo panel se pueden editar o eliminar publicaciones. Las fechas de creación y actualización se
completan solas; la fecha de publicación parte con el momento actual y se puede cambiar.

### Configuración del panel (`blog/admin.py`)

`PostAdmin` tiene 7 atributos:

| Atributo            | Valor                         | Efecto                                                       |
|---------------------|-------------------------------|--------------------------------------------------------------|
| `readonly_fields`   | `created`, `updated`          | Muestra las fechas automáticas sin permitir editarlas        |
| `list_display`      | `title`, `published`, `author`| Columnas del listado                                         |
| `ordering`          | `author`, `published`         | Orden del listado                                            |
| `search_fields`     | `title`, `author__name`       | Buscador por título o por nombre del autor                   |
| `date_hierarchy`    | `published`                   | Navegación por año / mes / día                               |
| `list_filter`       | `categories`, `author`        | Filtros en el panel lateral                                  |
| `filter_horizontal` | `categories`                  | Selector de categorías con dos cajas y buscador              |

## Cambios de la Evaluación 3

- **Modelos relacionados**: se agregaron `Category` (ManyToMany con `Post`) y `Author` (ForeignKey desde `Post`), y
  el campo `published`. La categoría con `choices` y el autor como texto se reemplazaron por estas relaciones.
- **Migración de datos**: se hizo en dos pasos para no perder las 11 publicaciones. `0002` creó las tablas nuevas;
  luego, con el shell de Django (`python manage.py shell`, usando el ORM), se crearon las 4 categorías y los 5
  autores, se asignaron a cada post y se copió `created` en `published`; `0003` quitó la categoría antigua y
  convirtió `author` en ForeignKey.
- **Vista de categoría**: `category(request, category_id)` con `get_object_or_404`, ruta
  `category/<category_id>/` y plantilla `blog/category.html`. Cada publicación muestra sus categorías como
  enlaces, el autor y la fecha en formato corto (`SHORT_DATE_FORMAT`). La lista lateral del blog se genera desde la BD.
- **Admin**: `PostAdmin` con 7 atributos; `Category`, `Author` y `BusinessInfo` registrados en el panel.
- **Procesador de contexto**: nueva app `info` con `processors.py`; la dirección, correos, teléfonos y horarios
  dejaron de estar escritos a mano en las plantillas.
- **Pruebas**: 33 pruebas (`python manage.py test`), incluidas las de la vista de categoría y del procesador.

## Créditos

- Diseño basado en la plantilla **Dopetrope** de [HTML5 UP](https://html5up.net), licencia
  [Creative Commons Attribution 3.0](https://html5up.net/license).
- Las fotografías con licencia Creative Commons (CC BY / CC BY-SA) se obtuvieron de Wikimedia Commons. El
  detalle de cada imagen, su autor y su licencia está en la sección **Créditos de imágenes** de la página
  Nosotros (`/about/#creditos`), enlazada también desde el pie de página.

## Integrantes

Ver [`web-plantas/INTEGRANTES.txt`](web-plantas/INTEGRANTES.txt).
