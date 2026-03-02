# Documentación del Módulo `musicians`

Este documento proporciona una descripción detallada de los modelos de datos y los endpoints de la API para el módulo `musicians` del proyecto Altempo.

## Modelos

A continuación se describen los modelos de Django definidos en `musicians/models.py`.

---

### `MusicProjectType`
Representa el tipo de proyecto musical (ej. "INDIVIDUAL", "BANDA").
- `name`: `CharField` - Nombre interno del tipo de proyecto.
- `display_name`: `CharField` - Nombre para mostrar en la interfaz.

---

### `TopicArtist`
Temas o tópicos que un artista puede abordar.
- `name`: `TextField` - El nombre del tema.
- `individual`: `BooleanField` - Indica si el tema es para perfiles individuales.

---

### `CategoryMusic`
Categorías musicales que agrupan géneros, idiomas, etc.
- `name`: `CharField` - Nombre de la categoría.
- `reference`: `CharField` - Referencia interna.
- `image`: `ImageField` - Imagen representativa.
- `music_genre_tags`: `ManyToManyField` a `MusicalGenreTag`.
- `languages`: `ManyToManyField` a `Language`.
- `topics`: `ManyToManyField` a `TopicArtist`.
- `orderservices`: `ManyToManyField` a `OrderServiceType`.
- `instruments`: `ManyToManyField` a `Instrument`.
- `typemusictext`: `CharField` - Texto descriptivo del tipo de música.
- `type_input`: `CharField` - Define el tipo de input en la UI ('select', 'multiple').
- `type_musician`: `CharField` - Define el tipo de músico ('vocalist', 'instrumentalist', etc.).

---

### `MusicProject`
El modelo central que representa el perfil de un músico o banda.
- `name`: `CharField` - Nombre del proyecto/artista.
- `slug`: `SlugField` - Identificador único para URLs.
- `description`: `TextField` - Descripción del proyecto.
- `owner`: `ForeignKey` a `User` - El usuario dueño del proyecto.
- `project_type`: `ForeignKey` a `MusicProjectType`.
- `members`: `ManyToManyField` a `User` - Miembros de la banda.
- `birth_date`: `DateField` - Fecha de nacimiento (para solistas).
- `phone_number`: `CharField` - Número de teléfono.
- `country`: `ForeignKey` a `Country`.
- `manager_name`: `CharField` - Nombre del mánager.
- `manager_number`: `CharField` - Teléfono del mánager.
- `biography`: `TextField` - Biografía del artista.
- `profile_image`: `ImageField` - Imagen de perfil.
- `cover_image`: `ImageField` - Imagen de portada.
- `years_of_experience`: `IntegerField`.
- `music_genre_tags`: `ManyToManyField` a `MusicalGenreTag`.
- `languages`: `ManyToManyField` a `Language`.
- `topics`: `ManyToManyField` a `TopicArtist`.
- `instruments`: `ManyToManyField` a `Instrument`.
- `categories`: `ManyToManyField` a `CategoryMusic`.
- `service_categories`: `ManyToManyField` a `services.Category`.
- `isProfileInfoCompleted`: `BooleanField` - Estado de completitud del perfil.
- `isVerificationStepsCompleted`: `BooleanField`.
- `isAvailabilityCompleted`: `BooleanField`.

---

### `Discography`
Representa un álbum o EP de un proyecto musical.
- `music_project`: `ForeignKey` a `MusicProject`.
- `title`: `CharField` - Título del álbum/EP.
- `type`: `CharField` - Tipo ('ALBUM', 'EP').
- `cover_image`: `ImageField` - Portada.
- `url_link`: `URLField` - Enlace a Spotify, Apple Music, etc.

---

### `Single`
Representa una canción individual.
- `music_project`: `ForeignKey` a `MusicProject`.
- `album`: `ForeignKey` a `Discography` (opcional).
- `title`: `CharField` - Título de la canción.
- `url_link`: `URLField` - Enlace a la canción.

---

### `InviteMemberBand`
Gestiona las invitaciones para unirse a una banda.
- `music_project`: `ForeignKey` a `MusicProject`.
- `invited_user`: `ForeignKey` a `User` (si el usuario ya existe).
- `inviter`: `ForeignKey` a `User` (quien envía la invitación).
- `email`: `CharField` - Email del invitado.
- `status`: `CharField` - Estado ('accepted', 'canceled', 'in_process').
- `message`: `TextField` - Mensaje personalizado.
- `expires_at`: `DateTimeField` - Fecha de expiración de la invitación.
- `responded_at`: `DateTimeField` - Fecha en que se respondió.

---

### `MusicProjectInstrument`
Relaciona un instrumento con un proyecto musical, especificando cantidad y precio.
- `music_project`: `ForeignKey` a `MusicProject`.
- `instrument`: `ForeignKey` a `Instrument`.
- `quantity`: `PositiveIntegerField` - Cantidad de este instrumento disponible.
- `price_per_instrument`: `DecimalField` - Precio por usar este instrumento.

---

### `InstrumentSet`
Agrupación de instrumentos para un servicio específico.
- `instrument_set_name`: `CharField`.
- `instruments_in_current_set`: `ManyToManyField` a `MusicProjectInstrument`.
- `music_project`: `ForeignKey` a `MusicProject`.

---

### `MusicProjectService`
Representa un servicio ofrecido por el músico.
- `music_project`: `ForeignKey` a `MusicProject`.
- `title`: `CharField`.
- `description`: `TextField`.
- `category`: `ForeignKey` a `services.Category`.
- `item`: `ForeignKey` a `services.Item`.
- `specific_service`: `ForeignKey` a `services.SpecificService`.
- `is_active`: `BooleanField`.
- `modes`: `ManyToManyField` a `ServiceMode`.
- `selected_instrument_set`: `ForeignKey` a `MusicProjectInstrumentInstrumentSet`.

---

### `MusicProjectVideo` y `MusicProjectVideoDraft`
Gestionan los videos del perfil del músico. `MusicProjectVideoDraft` es para videos pendientes de aprobación por un administrador.
- `music_project`: `ForeignKey` a `MusicProject`.
- `video_url`: `URLField`.
- `caption`: `TextField`.
- `status`: `CharField` (solo en Draft) - Estado de la revisión.
- `feedback`: `TextField` (solo en Draft) - Comentarios del revisor.

---

## Endpoints de la API

A continuación se describen los endpoints definidos en `musicians/urls.py`.

---

### Listar Tipos de Proyecto Musical
- **Path:** `/api/music-project-types/`
- **Método:** `GET`
- **Permisos:** `AllowAny` (según `drf-spectacular`, aunque la vista no especifica permisos, podría heredar de la configuración global).
- **Descripción:** Devuelve una lista de todos los tipos de proyectos musicales disponibles.
- **Respuesta Exitosa (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "INDIVIDUAL",
      "display_name": "Solista"
    },
    {
      "id": 2,
      "name": "BAND",
      "display_name": "Banda"
    }
  ]
  ```

---

### Crear un Proyecto Musical
- **Path:** `/api/music-project/`
- **Método:** `POST`
- **Permisos:** `IsAuthenticated`
- **Descripción:** Crea un nuevo proyecto musical para el usuario autenticado.
- **Cuerpo de la Petición:**
  ```json
  {
    "music_project_name": "Mi Proyecto Acústico",
    "music_project_type_id": 1,
    "services": [10, 12]
  }
  ```
- **Respuesta Exitosa (201 Created):** Devuelve el objeto `MusicProject` completo recién creado.

---

### Obtener/Actualizar/Eliminar Detalles de un Proyecto Musical
- **Path:** `/api/musician/projects/<int:pk>/`
- **Métodos:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Permisos:** `IsMusicProjectOwnerOrReadOnly`
- **Descripción:** Gestiona un proyecto musical específico. Permite obtener detalles, actualizarlo parcial o totalmente, o eliminarlo.
- **Parámetros de URL:**
  - `pk`: ID del `MusicProject`.
- **Cuerpo de la Petición (PATCH):**
  ```json
  {
    "name": "Nuevo Nombre de la Banda",
    "biography": "Una nueva biografía actualizada.",
    "languages": [1, 3]
  }
  ```
- **Respuesta Exitosa (200 OK):** Devuelve el objeto `MusicProject` actualizado.

---

### Listar y Crear Álbumes (Discografía)
- **Path:** `/api/musician/projects/<int:pk>/albums/`
- **Métodos:** `GET`, `POST`
- **Permisos:** `IsAuthenticated`, `IsMusicProjectOwnerOrReadOnly`
- **Descripción:** Lista los álbumes de un proyecto o crea uno nuevo.
- **Parámetros de URL:**
  - `pk`: ID del `MusicProject`.
- **Cuerpo de la Petición (POST):** `form-data` con los campos `title`, `type`, `url_link`, y `cover_image` (archivo).
- **Respuesta Exitosa (200 OK / 201 Created):**
  ```json
  {
    "id": 1,
    "title": "Mi Primer Álbum",
    "cover_image": "/media/path/to/image.jpg",
    "url_link": "https://spotify.com/album/123",
    "music_project": 1,
    "type": "ALBUM"
  }
  ```

---

### Enviar Invitación a un Miembro
- **Path:** `/api/musician/projects/<int:pk>/invitations/`
- **Método:** `POST`
- **Permisos:** `IsAuthenticated`, `IsMusicProjectOwnerOrReadOnly`
- **Descripción:** Envía una invitación por correo para unirse a un proyecto musical.
- **Parámetros de URL:**
  - `pk`: ID del `MusicProject`.
- **Cuerpo de la Petición:**
  ```json
  {
    "email": "nuevo.miembro@example.com",
    "message": "¡Hola! Te invito a unirte a mi banda."
  }
  ```
- **Respuesta Exitosa (201 Created):**
  ```json
  {
    "message": "Invitation sent successfully.",
    "invitation_id": 5,
    "email": "nuevo.miembro@example.com"
  }
  ```

---

### Aceptar una Invitación
- **Path:** `/api/invitations/<int:invitation_id>/accept/`
- **Método:** `POST`
- **Permisos:** `IsAuthenticated`
- **Descripción:** Acepta una invitación para unirse a una banda. El usuario autenticado debe ser el destinatario de la invitación.
- **Parámetros de URL:**
  - `invitation_id`: ID de la `InviteMemberBand`.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "message": "Invitación aceptada con éxito."
  }
  ```

---

### Gestionar Instrumentos del Proyecto
- **Path:** `/api/musician/projects/<int:pk>/instruments/`
- **Métodos:** `GET`, `POST`
- **Permisos:** `IsAuthenticated`
- **Descripción:** Lista los instrumentos de un proyecto o añade uno nuevo.
- **Parámetros de URL:**
  - `pk`: ID del `MusicProject`.
- **Cuerpo de la Petición (POST):**
  ```json
  {
    "instrument_id": 5,
    "quantity": 2,
    "price_per_instrument": 50.00
  }
  ```
- **Respuesta Exitosa (201 Created):** Devuelve el objeto `MusicProjectInstrument` creado.

---

### Gestionar Servicios del Proyecto
- **Path:** `/api/musician/projects/<int:pk>/services/`
- **Métodos:** `GET`, `POST`
- **Permisos:** `IsAuthenticated`
- **Descripción:** Lista los servicios de un proyecto o crea uno nuevo.
- **Parámetros de URL:**
  - `pk`: ID del `MusicProject`.
- **Cuerpo de la Petición (POST):**
  ```json
  {
    "title": "Clases de Guitarra Online",
    "description": "Aprende a tocar la guitarra desde cero.",
    "category_id": "clases",
    "service_item_id": "instrumento",
    "sub_service_id": "guitarra",
    "pricing_intervals": [
        {"price": 25.00, "duration": 1, "unit": "hour", "is_base": true}
    ],
    "attributes": {"nivel": "principiante"}
  }
  ```
- **Respuesta Exitosa (201 Created):** Devuelve el objeto `MusicProjectService` creado.

---

### Gestionar Disponibilidad
- **Path:** `/api/musician/projects/<int:pk>/availability/`
- **Métodos:** `GET`, `PATCH`
- **Permisos:** `IsAuthenticated`
- **Descripción:** Obtiene o actualiza la información de disponibilidad del músico (horarios semanales y fechas específicas).
- **Parámetros de URL:**
  - `pk`: ID del `MusicProject`.
- **Cuerpo de la Petición (PATCH):**
  ```json
  {
    "time_schedule": [
      {
        "day": "monday",
        "start_time": "09:00:00",
        "end_time": "17:00:00"
      }
    ],
    "day_schedule": [
      {
        "date": "2025-12-24",
        "modality": "on_site"
      }
    ]
  }
  ```
- **Respuesta Exitosa (200 OK):** Devuelve el objeto `AvailabilityInfo` actualizado.
