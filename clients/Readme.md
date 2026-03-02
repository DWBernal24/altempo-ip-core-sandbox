# Documentación de la Aplicación `clients`

Esta aplicación gestiona los tipos de clientes, detalles y dificultades de incorporación en Altempo.

## Modelos

A continuación se describen los modelos de datos para la aplicación `clients`.

### `ClientType`

Representa un tipo de cliente.

| Campo          | Tipo        | Descripción                              |
|----------------|-------------|------------------------------------------|
| `name`         | CharField   | El nombre del tipo de cliente (único).   |
| `display_name` | CharField   | El nombre a mostrar (único, opcional).   |
| `image`        | ImageField  | Una imagen para el tipo de cliente (opcional). |

### `ClientDetail`

Proporciona detalles específicos para un tipo de cliente.

| Campo                | Tipo         | Descripción                                                  |
|----------------------|--------------|--------------------------------------------------------------|
| `name`               | CharField    | El nombre del detalle.                                       |
| `client_type`        | ForeignKey   | Relación con `ClientType`.                                   |
| `allows_custom_text` | BooleanField | Indica si se permite texto personalizado. Por defecto es `False`. |
| `image`              | ImageField   | Una imagen para el detalle del cliente (opcional).           |
| `sequence`           | IntegerField | El orden de secuencia para la visualización. Por defecto es `0`. |

### `ClientOnboardingDifficulty`

Describe una dificultad de incorporación asociada a un rol.

| Campo         | Tipo         | Descripción                                                  |
|---------------|--------------|--------------------------------------------------------------|
| `role`        | ForeignKey   | Relación con el modelo `Role`.                               |
| `description` | TextField    | Una descripción de la dificultad.                            |
| `sequence`    | IntegerField | El orden de secuencia para la visualización. Por defecto es `0`. |

### `UserProfileOnboardingDifficulty`

Vincula el perfil de un usuario con una dificultad de incorporación específica.

| Campo                | Tipo         | Descripción                                                              |
|----------------------|--------------|--------------------------------------------------------------------------|
| `user_profile`       | ForeignKey   | Relación con el modelo `UserProfile`.                                    |
| `difficulty`         | ForeignKey   | Relación con `ClientOnboardingDifficulty`.                               |
| `custom_description` | TextField    | Una descripción personalizada para la dificultad del usuario (opcional). |

---

## API Endpoints

A continuación se detallan los endpoints de la API para la aplicación `clients`.

### 1. Listar Tipos de Cliente

- **Endpoint:** `GET /api/clients/types/`
- **Descripción:** Obtiene una lista paginada de todos los tipos de cliente.
- **Parámetros de Consulta:** Ninguno.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Corporate",
        "display_name": "Corporate Client",
        "image": "http://example.com/media/clients/client_types/image.jpg"
      }
    ]
  }
  ```

### 2. Listar Detalles de Cliente

- **Endpoint:** `GET /api/clients/details/`
- **Descripción:** Obtiene una lista paginada de detalles de cliente, con la opción de filtrar por tipo de cliente.
- **Parámetros de Consulta:**
  - `client_type` (opcional): El `id` del tipo de cliente para filtrar los resultados.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Detail Name",
        "client_type": 1,
        "allows_custom_text": false,
        "image": "http://example.com/media/clients/client_detail/image.jpg",
        "sequence": 1
      }
    ]
  }
  ```

### 3. Listar Dificultades de Incorporación de Clientes

- **Endpoint:** `GET /api/clients/difficulties/`
- **Descripción:** Obtiene una lista paginada de dificultades de incorporación, con la opción de filtrar por rol.
- **Parámetros de Consulta:**
  - `role` (opcional): El `id` del rol para filtrar los resultados.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "role": 1,
        "description": "High difficulty",
        "sequence": 1
      }
    ]
  }
  ```
