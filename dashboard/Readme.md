
# Documentación del Módulo de Dashboard

Este módulo proporciona los endpoints de la API para que los administradores gestionen varios aspectos de la plataforma, como proyectos musicales, videos y otros datos.

## Modelos (Serializadores)

La aplicación `dashboard` no tiene modelos de Django propios. En su lugar, utiliza serializadores para representar datos de modelos de otras aplicaciones como `musicians`, `core` y `services`. A continuación se detallan los principales serializadores utilizados.

### `AdminTokenObtainPairSerializer`

Este serializador se utiliza para el inicio de sesión del administrador. Extiende el serializador de tokens JWT para incluir datos del usuario en la respuesta.

**Campos de Respuesta:**

- `access` (string): Token de acceso JWT.
- `refresh` (string): Token de refresco JWT.
- `user` (object): Información del usuario autenticado.
  - `pk` (integer): ID del usuario.
  - `username` (string): Nombre de usuario.
  - `email` (string): Correo electrónico del usuario.
  - `first_name` (string): Nombre del usuario.
  - `last_name` (string): Apellido del usuario.

### `LeanMusicProjectSerializer`

Proporciona una representación simplificada de un `MusicProject`.

**Campos:**

- `id` (integer): ID del proyecto musical.
- `name` (string): Nombre del proyecto musical.
- `service_categories` (array): Lista de categorías de servicios (`LeanCategorySerializer`).
  - `id` (integer): ID de la categoría.
  - `name` (string): Nombre de la categoría.
  - `display_name` (string): Nombre para mostrar de la categoría.
- `isProfileInfoCompleted` (boolean): Indica si la información del perfil está completa.
- `isVerificationStepsCompleted` (boolean): Indica si los pasos de verificación están completos.
- `isAvailabilityCompleted` (boolean): Indica si la disponibilidad está completa.
- `owner` (object): Propietario del proyecto (`LeanUserSerializer`).
  - `id` (integer): ID del usuario.
  - `email` (string): Correo electrónico del usuario.
  - `name` (string): Nombre del usuario.

### `ReviewMusicProjectVideoDraftSerializer`

Se utiliza para la revisión de borradores de videos de proyectos musicales.

**Campos:**

- `id` (integer, read-only): ID del borrador del video.
- `music_project` (object, read-only): Proyecto musical asociado (`LeanMusicProjectSerializer`).
- `status` (string, required): Estado de la revisión. Opciones: `INPROCESS`, `ACCEPTED`, `REJECTED`.
- `feedback` (string): Comentarios de la revisión.
- `reviewed_by` (integer, read-only): ID del administrador que revisó.
- `reviewed_at` (datetime, read-only): Fecha y hora de la revisión.
- `video_url` (string): URL del video.
- `caption` (string): Título o descripción del video.

---

## Documentación de Endpoints de la API

A continuación se describen los endpoints disponibles en el módulo de dashboard. Todos los endpoints requieren permisos de administrador.

### Autenticación

#### 1. Admin Login

- **Path:** `/login/`
- **Método:** `POST`
- **Descripción:** Autentica a un usuario como administrador y devuelve tokens JWT.
- **Permisos:** Público (pero solo los administradores recibirán una respuesta exitosa).
- **Cuerpo de la Solicitud (Request Body):**
  ```json
  {
    "username": "admin_user",
    "password": "admin_password"
  }
  ```
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "pk": 1,
      "username": "admin_user",
      "email": "admin@example.com",
      "first_name": "Admin",
      "last_name": "User"
    }
  }
  ```

### Proyectos Musicales

#### 2. Listar Proyectos Musicales

- **Path:** `/music-projects/`
- **Método:** `GET`
- **Descripción:** Obtiene una lista paginada de todos los proyectos musicales.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Consulta (Query Parameters):**
  - `search` (string, opcional): Filtra los proyectos por nombre.
  - `completion` (string, opcional): Filtra por estado de finalización del perfil. Opciones: `completed`, `pending`.
- **Respuesta Exitosa (200 OK):** Lista paginada de objetos `LeanMusicProjectSerializer`.

#### 3. Detalles de un Proyecto Musical

- **Path:** `/music-projects/<int:pk>/`
- **Métodos:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Descripción:** Obtiene, actualiza o elimina un proyecto musical específico.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta (Path Parameters):**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta Exitosa (200 OK):** Objeto `MusicProjectSerializer` completo.

#### 4. Listar y Crear Álbumes de un Proyecto Musical

- **Path:** `/music-projects/<int:pk>/albums/`
- **Métodos:** `GET`, `POST`
- **Descripción:** Lista los álbumes (discografía) de un proyecto o crea uno nuevo.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta (GET):** Lista paginada de objetos `DiscographySerializer`.
- **Respuesta (POST):** Objeto `DiscographySerializer` del álbum creado.

#### 5. Listar Instrumentos de un Proyecto Musical

- **Path:** `/music-projects/<int:pk>/instruments/`
- **Método:** `GET`
- **Descripción:** Lista los instrumentos asociados a un proyecto musical.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta:** Lista paginada de objetos `MusicProjectInstrumentsSerializer`.

#### 6. Listar Conjuntos de Instrumentos (Instrument Sets)

- **Path:** `/music-projects/<int:pk>/instrument-sets/`
- **Método:** `GET`
- **Descripción:** Lista los conjuntos de instrumentos de un proyecto musical.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta:** Lista de objetos `InstrumentSetSerializer`.

#### 7. Listar Servicios de un Proyecto Musical

- **Path:** `/music-projects/<int:pk>/services/`
- **Método:** `GET`
- **Descripción:** Lista los servicios ofrecidos por un proyecto musical.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta:** Lista de objetos `MusicProjectServiceSerializer`.

#### 8. Listar Sencillos (Singles) de un Proyecto Musical

- **Path:** `/music-projects/<int:pk>/singles/`
- **Método:** `GET`
- **Descripción:** Lista los sencillos de un proyecto musical.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta:** Lista paginada de objetos `SingleSerializer`.

### Revisión de Videos

#### 9. Revisar un Borrador de Video

- **Path:** `/music-projects/<int:pk>/videos/<int:draft_pk>/review/`
- **Métodos:** `GET`, `PUT`, `PATCH`
- **Descripción:** Obtiene o actualiza el estado de revisión de un borrador de video.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
  - `draft_pk` (integer): ID del borrador de video.
- **Cuerpo de la Solicitud (PUT/PATCH):**
  ```json
  {
    "status": "ACCEPTED",
    "feedback": "¡Buen trabajo!"
  }
  ```
- **Respuesta (GET):** Objeto `ReviewMusicProjectVideoDraftSerializer`.
- **Respuesta (PUT/PATCH, 200 OK):** Mensaje de confirmación.

#### 10. Listar Borradores de Video de un Proyecto

- **Path:** `/music-projects/<int:pk>/videos/`
- **Método:** `GET`
- **Descripción:** Lista todos los borradores de video para un proyecto musical específico.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Ruta:**
  - `pk` (integer): ID del proyecto musical.
- **Respuesta:** Lista paginada de objetos `ReviewMusicProjectVideoDraftSerializer`.

#### 11. Listar Borradores de Video Pendientes

- **Path:** `/drafts/pending/`
- **Método:** `GET`
- **Descripción:** Lista todos los borradores de video de la plataforma con un estado específico.
- **Permisos:** `IsAdministrator`.
- **Parámetros de Consulta:**
  - `status` (string, opcional): Filtra por estado. Opciones: `INPROCESS`, `ACCEPTED`, `REJECTED`. Por defecto, devuelve todos.
- **Respuesta:** Lista paginada de objetos `ReviewMusicProjectVideoDraftSerializer`.
