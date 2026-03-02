
# Documentación de la Aplicación Core

Esta aplicación contiene los modelos y endpoints principales para la funcionalidad de Altempo.

## Modelos

A continuación se describen los modelos de la aplicación `core`:

### Country

Almacena información sobre los países.

- `name`: Nombre del país (cadena, único).
- `iso_code`: Código ISO del país (cadena, 2 caracteres, único).

### ReferralSource

Almacena las fuentes de referencia a través de las cuales los usuarios conocen la plataforma.

- `name`: Nombre de la fuente de referencia (cadena, único).

### Gender

Almacena los géneros con los que se pueden identificar los usuarios.

- `name`: Nombre del género (cadena, único).
- `sequence`: Entero para ordenar los géneros.

### MusicalGenreTag

Etiquetas para los géneros musicales.

- `name`: Nombre del género musical (cadena, único).

### InstrumentType

Tipos de instrumentos musicales.

- `name`: Nombre del tipo de instrumento (cadena, único).

### Instrument

Instrumentos musicales que un músico puede tocar.

- `name`: Nombre del instrumento (cadena, único).
- `description`: Descripción del instrumento (texto, opcional).
- `type`: Tipo de instrumento (clave foránea a `InstrumentType`, opcional).

### MusicianVoiceType

Tipos de voz para los músicos.

- `name`: Nombre del tipo de voz (cadena, único).
- `description`: Descripción del tipo de voz (texto, opcional).

### VocalStyle

Estilos vocales que un músico puede tener.

- `name`: Nombre del estilo vocal (cadena, único).
- `description`: Descripción del estilo vocal (texto, opcional).

### CollabType

Tipos de colaboración que se pueden realizar.

- `name`: Nombre del tipo de colaboración (cadena, único).
- `description`: Descripción del tipo de colaboración (texto, opcional).

### DJType

Tipos de DJ.

- `name`: Nombre del tipo de DJ (cadena, único).
- `description`: Descripción del tipo de DJ (texto, opcional).

### Equipment

Equipamiento que puede ser necesario para un evento.

- `name`: Nombre del equipo (cadena, único).
- `description`: Descripción del equipo (texto, opcional).
- `inventory`: Cantidad de equipo disponible (entero positivo pequeño).
- `image`: Imagen del equipo (archivo de imagen, opcional).

### Language

Idiomas que los usuarios pueden hablar.

- `code`: Código del idioma (cadena, único).
- `name`: Nombre del idioma (cadena, único).

### Notification

Notificaciones para los usuarios.

- `title`: Título de la notificación (cadena).
- `message`: Mensaje corto de la notificación (texto).
- `type`: Tipo de notificación (cadena, con opciones predefinidas).
- `user`: Usuario que recibe la notificación (clave foránea a `User`).
- `created_at`: Fecha y hora de creación de la notificación.
- `read`: Booleano que indica si la notificación ha sido leída.
- `value`: Valor adicional para redireccionamiento (texto, opcional).
- `detail`: Mensaje más detallado (texto, opcional).

## Endpoints

A continuación se describen los endpoints de la API para la aplicación `core`:

### `GET /core/countries/`

Obtiene una lista de todos los países.

- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "name": "Country Name",
      "iso_code": "CN"
    }
  ]
  ```

### `GET /core/timezones/`

Obtiene una lista de zonas horarias comunes.

- **Respuesta:**
  ```json
  {
    "count": 31,
    "timezones": [
      {
        "value": "UTC",
        "label": "UTC",
        "offset": "+0000",
        "display": "UTC (UTC+0000)"
      }
    ]
  }
  ```

### `GET /core/referral-sources/`

Obtiene una lista de todas las fuentes de referencia.

- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "name": "Referral Source Name"
    }
  ]
  ```

### `GET /core/genders/`

Obtiene una lista de todos los géneros.

- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "name": "Gender Name",
      "sequence": 0
    }
  ]
  ```

### `GET /core/musical-genres/`

Obtiene una lista paginada de géneros musicales.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Musical Genre Name"
      }
    ]
  }
  ```

### `GET /core/musician-voices-types/`

Obtiene una lista paginada de tipos de voz de músicos.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Voice Type Name",
        "description": "Description"
      }
    ]
  }
  ```

### `GET /core/vocal-styles/`

Obtiene una lista paginada de estilos vocales.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Vocal Style Name",
        "description": "Description"
      }
    ]
  }
  ```

### `GET /core/instruments/`

Obtiene una lista de todos los instrumentos.

- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "name": "Instrument Name",
      "description": "Description",
      "type": 1
    }
  ]
  ```

### `GET /core/dj-types/`

Obtiene una lista paginada de tipos de DJ.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "DJ Type Name",
        "description": "Description"
      }
    ]
  }
  ```

### `GET /core/collab-types/`

Obtiene una lista paginada de tipos de colaboración.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Collab Type Name",
        "description": "Description"
      }
    ]
  }
  ```

### `GET /core/equipment/`

Obtiene una lista paginada de equipamiento.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Equipment Name",
        "description": "Description",
        "inventory": 0,
        "image": null
      }
    ]
  }
  ```

### `GET /core/languages/`

Obtiene una lista paginada de idiomas.

- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "code": "en",
        "name": "English"
      }
    ]
  }
  ```

### `GET /core/notifications/`

Obtiene una lista paginada de notificaciones para el usuario autenticado. Requiere autenticación.

- **Parámetros de consulta:**
  - `last_event_id` (opcional): Filtra las notificaciones con un ID mayor que el proporcionado.
  - `notification_type` (opcional): Filtra las notificaciones por tipo.
- **Respuesta:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Notification Title",
        "message": "Notification Message",
        "type": "PROFILE_COMPLETED",
        "user": 1,
        "created_at": "2023-10-27T10:00:00Z",
        "read": false,
        "value": null,
        "detail": null
      }
    ]
  }
  ```

### `PATCH /core/notifications/<int:pk>/`

Marca una notificación específica como leída. Requiere autenticación.

- **Parámetros de URL:**
  - `pk`: ID de la notificación.
- **Respuesta:**
  ```json
  {
    "success": true
  }
  ```
