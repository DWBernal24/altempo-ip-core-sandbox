# Documentación de la Aplicación "roles"

## Modelos

A continuación se describen los modelos de la aplicación `roles`.

### `Role`

Define los roles que un usuario puede tener en el sistema.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único del rol (ej. `MUSICIAN`, `TALENT_HUNTER`). |
| `display_name` | `CharField` | Nombre para mostrar del rol. |
| `image` | `ImageField` | Imagen representativa del rol (opcional). |

### `UserProfile`

Almacena información adicional del perfil de un usuario, extendiendo el modelo `User` de Django.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `user` | `OneToOneField` | Relación uno a uno con el modelo `User`. |
| `name` | `CharField` | Nombre completo del usuario. |
| `role` | `ForeignKey` | Rol del usuario en el sistema. |
| `client_type` | `ForeignKey` | Tipo de cliente (si aplica). |
| `client_detail` | `ForeignKey` | Detalle del cliente (si aplica). |
| `custom_client_detail` | `CharField` | Detalle personalizado del cliente. |
| `country` | `ForeignKey` | País del usuario. |
| `birth_date` | `DateField` | Fecha de nacimiento. |
| `gender` | `ForeignKey` | Género del usuario. |
| `phone_number` | `CharField` | Número de teléfono. |
| `referral_source` | `ForeignKey` | Cómo conoció el usuario la plataforma. |
| `status` | `CharField` | Estado del perfil (`draft`, `pending_review`, `approved`, `rejected`). |
| `verified` | `BooleanField` | Indica si el perfil ha sido verificado. |
| `language` | `ForeignKey` | Idioma preferido del usuario. |
| `timezone` | `CharField` | Zona horaria del usuario (formato IANA). |
| `role_company` | `CharField` | Rol o cargo en la empresa (para Talent Hunters). |
| `category` | `ForeignKey` | Categoría principal de interés (para Talent Hunters). |
| `subcategories` | `ManyToManyField` | Subcategorías de interés. |
| `contracting_modalty` | `CharField` | Modalidad de contratación preferida. |
| `address` | `CharField` | Dirección. |
| `city` | `CharField` | Ciudad. |
| `frecuency` | `CharField` | Frecuencia de contratación. |

### `Demografy`

Define características demográficas que pueden ser asociadas a un perfil.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre de la característica demográfica (ej. "Jóvenes", "Familias"). |
| `other` | `BooleanField` | Indica si es una opción "otro" que permite texto libre. |

### `ListDemografyProfile`

Asocia una característica demográfica a un perfil de usuario.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `demografy` | `ForeignKey` | Característica demográfica. |
| `is_other` | `BooleanField` | Indica si se usó la opción "otro". |
| `other_name` | `CharField` | Valor personalizado si `is_other` es verdadero. |
| `profile` | `ForeignKey` | Perfil de usuario al que se asocia. |

### `KeyDates`

Define fechas o eventos clave que pueden ser relevantes para un perfil.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre de la fecha clave (ej. "Aniversarios", "Lanzamientos"). |
| `other` | `BooleanField` | Indica si es una opción "otro". |

### `KeyDatesProfile`

Asocia una fecha clave a un perfil de usuario.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `key_dates` | `ForeignKey` | Fecha clave. |
| `is_other` | `BooleanField` | Indica si se usó la opción "otro". |
| `other_name` | `CharField` | Valor personalizado si `is_other` es verdadero. |
| `profile` | `ForeignKey` | Perfil de usuario al que se asocia. |

### `UserCategory`

Asocia un usuario a una categoría de servicio, con un estado de aprobación.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `user_profile` | `ForeignKey` | Perfil del usuario. |
| `category` | `ForeignKey` | Categoría de servicio. |
| `status` | `CharField` | Estado de la asociación (`pending`, `approved`, `rejected`). |

### `Gallery`

Galería de imágenes de un usuario.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `user` | `OneToOneField` | Usuario al que pertenece la galería. |
| `image` | `ImageField` | Imagen de la galería. |

### `Album`

Álbumes de música de un usuario (links externos).

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `user` | `OneToOneField` | Usuario al que pertenece el álbum. |
| `name` | `TextField` | Nombre del álbum. |
| `link` | `TextField` | Enlace al álbum. |
| `type` | `CharField` | Plataforma del álbum (`YOUTUBE`, `SPOTIFY`, `OTHER`). |

---

## Endpoints de la API

A continuación se detallan los endpoints disponibles en la aplicación `roles`.

### Roles

- **`GET /api/roles/`**
  - **Descripción:** Obtiene la lista de roles disponibles en el sistema.
  - **Respuesta:** Lista paginada de objetos `Role`.

- **`POST /api/roles/`**
  - **Descripción:** Crea un nuevo rol (generalmente para uso administrativo).
  - **Cuerpo (Body):** Objeto `RoleSerializer` con los datos del nuevo rol.
  - **Respuesta:** Objeto `Role` creado.

### Perfil de Usuario (UserProfile)

- **`POST /api/users/profile`**
  - **Descripción:** Crea o actualiza el perfil de un usuario. Requiere autenticación.
  - **Cuerpo (Body):** Objeto `UserProfileSerializer` con los datos del perfil.
  - **Respuesta:** Objeto `UserProfile` creado o actualizado.

- **`GET /api/me/profile/`**
  - **Descripción:** Obtiene el perfil del usuario autenticado.
  - **Respuesta:** Objeto `UserProfileGetSerializer` con los datos del perfil.

### Demografía y Fechas Clave

- **`GET /api/demografy/`**
  - **Descripción:** Obtiene la lista de opciones de demografía base.
  - **Respuesta:** Lista paginada de objetos `Demografy`.

- **`GET /api/keydates/`**
  - **Descripción:** Obtiene la lista de opciones de fechas clave base.
  - **Respuesta:** Lista paginada de objetos `KeyDates`.

- **`GET /api/list-demografy-profile/`**
  - **Descripción:** Obtiene las características demográficas asociadas al perfil del usuario autenticado.
  - **Respuesta:** Lista paginada de objetos `ListDemografyProfile`.

- **`POST /api/list-demografy-profile/`**
  - **Descripción:** Asocia una nueva característica demográfica al perfil del usuario.
  - **Cuerpo (Body):** Objeto `ListDemografyProfileSerializer`.
  - **Respuesta:** Objeto `ListDemografyProfile` creado.

- **`DELETE /api/list-demografy-profile/`**
  - **Descripción:** Elimina una característica demográfica del perfil del usuario.
  - **Parámetros (Query):** `id` (ID del registro `ListDemografyProfile`).
  - **Respuesta:**
    ```json
    {
      "message": "Parametro no definido"
    }
    ```

- **`GET /api/list-keydates-profile/`**
  - **Descripción:** Obtiene las fechas clave asociadas al perfil del usuario autenticado.
  - **Respuesta:** Lista paginada de objetos `KeyDatesProfile`.

- **`POST /api/list-keydates-profile/`**
  - **Descripción:** Asocia una nueva fecha clave al perfil del usuario.
  - **Cuerpo (Body):** Objeto `KeyDatesProfileSerializer`.
  - **Respuesta:** Objeto `KeyDatesProfile` creado.

- **`DELETE /api/list-keydates-profile/`**
  - **Descripción:** Elimina una fecha clave del perfil del usuario.
  - **Parámetros (Query):** `id` (ID del registro `KeyDatesProfile`).
  - **Respuesta:**
    ```json
    {
      "message": "Parametro no definido"
    }
    ```
