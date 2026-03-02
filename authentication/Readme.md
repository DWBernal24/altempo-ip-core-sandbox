# Documentación del Módulo de Autenticación

Este documento proporciona una descripción detallada de los modelos de datos y los endpoints de la API para el módulo de autenticación y gestión de perfiles de usuario.

## Modelos

La aplicación `authentication` no define modelos de Django directamente. En su lugar, utiliza y amplía el modelo de usuario predeterminado de Django a través de un perfil de usuario definido en la aplicación `roles`.

### `UserProfile` (`roles.models.UserProfile`)

Este modelo contiene toda la información adicional del perfil de un usuario.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `user` | OneToOneField | Relación uno a uno con el modelo `User` de Django. |
| `name` | CharField | Nombre completo del usuario. |
| `role` | ForeignKey | El rol del usuario (ej. Músico, Cazatalentos). |
| `client_type` | ForeignKey | Tipo de cliente (si aplica). |
| `client_detail` | ForeignKey | Detalles específicos del cliente. |
| `custom_client_detail` | CharField | Detalles personalizados del cliente si no hay una opción. |
| `country` | ForeignKey | País del usuario. |
| `birth_date` | DateField | Fecha de nacimiento del usuario. |
| `gender` | ForeignKey | Género del usuario. |
| `phone_number` | CharField | Número de teléfono del usuario. |
| `referral_source` | ForeignKey | Cómo el usuario conoció la plataforma. |
| `status` | CharField | Estado del perfil (ej. Borrador, Aprobado). |
| `verified` | BooleanField | Indica si la cuenta de correo ha sido verificada. |
| `language` | ForeignKey | Idioma preferido del usuario. |
| `timezone` | CharField | Zona horaria del usuario (formato IANA, ej. "UTC"). |
| `role_company` | CharField | Rol o cargo en la empresa (para Cazatalentos). |
| `category` | ForeignKey | Categoría principal de interés (para Cazatalentos). |
| `subcategories` | ManyToManyField | Subcategorías de interés. |
| `contracting_modalty` | CharField | Modalidad de contratación preferida. |
| `address` | CharField | Dirección del Cazatalentos. |
| `city` | CharField | Ciudad del Cazatalentos. |
| `frecuency` | CharField | Frecuencia de contratación. |

---

## Endpoints de la API

A continuación se detallan los endpoints disponibles en `/api/auth/`.

### Registro

#### `POST /api/auth/register/musician/`
- **Descripción:** Registra un nuevo usuario con el rol de "Músico".
- **Parámetros del Body:**
  - `name` (string, requerido)
  - `email` (string, requerido)
  - `password` (string, requerido)
  - `id_country` (integer, requerido)
  - `id_referral_source` (integer, requerido)
  - `phone_number` (string, opcional)
  - `id_services` (array de integers, opcional): IDs de los servicios que ofrece.
- **Respuesta:**
  - `201 OK`: Devuelve un token de acceso y de refresco.

#### `POST /api/auth/register/talent-hunter/`
- **Descripción:** Registra un nuevo usuario con el rol de "Cazatalentos".
- **Parámetros del Body:**
  - `name` (string, requerido)
  - `email` (string, requerido)
  - `password` (string, requerido)
  - `id_country` (integer, requerido)
  - `id_referral_source` (integer, requerido)
  - `phone_number` (string, opcional)
  - `id_client_type` (integer, opcional)
  - `id_client_detail` (integer, opcional)
  - `other_client_detail` (string, opcional)
- **Respuesta:**
  - `201 OK`: Devuelve un token de acceso y de refresco.

### Autenticación

#### `POST /api/auth/login/`
- **Descripción:** Inicia sesión de un usuario.
- **Parámetros del Body:**
  - `email` (string, requerido)
  - `password` (string, requerido)
- **Respuesta:**
  - `200 OK`: Devuelve un token de acceso y de refresco, junto con detalles del usuario.

#### `POST /api/auth/logout/`
- **Descripción:** Cierra la sesión del usuario. Requiere autenticación.
- **Respuesta:**
  - `200 OK`: `{"detail": "Successfully logged out."}`

#### `POST /api/auth/google/`
- **Descripción:** Autenticación a través de Google.
- **Parámetros del Body:**
  - `access_token` (string, requerido): Token de acceso proporcionado por Google.
- **Respuesta:**
  - `200 OK`: Devuelve un token de acceso y de refresco de la aplicación.

### Gestión de Tokens

#### `POST /api/auth/token/verify/`
- **Descripción:** Verifica la validez de un token de acceso.
- **Parámetros del Body:**
  - `token` (string, requerido)
- **Respuesta:**
  - `200 OK`: `{}` (si el token es válido).
  - `401 Unauthorized`: Si el token es inválido o ha expirado.

#### `POST /api/auth/token/refresh/`
- **Descripción:** Obtiene un nuevo token de acceso usando un token de refresco.
- **Parámetros del Body:**
  - `refresh` (string, requerido)
- **Respuesta:**
  - `200 OK`: `{"access": "..."}`

### Gestión de Perfil y Cuenta

#### `GET /api/auth/user/`
- **Descripción:** Obtiene los detalles del usuario autenticado. Requiere autenticación.
- **Respuesta:**
  - `200 OK`: Devuelve los datos del usuario (`pk`, `username`, `email`, `name`).

#### `GET, PUT /api/auth/profile/`
- **Descripción:** Permite obtener y actualizar el perfil del usuario autenticado. Requiere autenticación.
- **Método `GET`:**
  - **Respuesta:** `200 OK` con los datos del `UserProfile`.
- **Método `PUT`:**
  - **Parámetros del Body:** Campos del `UserProfile` a actualizar.
  - **Respuesta:** `200 OK` con el perfil actualizado.

### Verificación de Correo

#### `POST /api/auth/verify/send/`
- **Descripción:** Envía (o reenvía) un correo de verificación a la dirección de correo del usuario autenticado. Requiere autenticación.
- **Respuesta:**
  - `200 OK`: `{"message": "Verification email sent"}`

#### `GET /api/auth/verify/user/<uidb64>/<token>/`
- **Descripción:** Verifica la cuenta de un usuario a través del enlace enviado por correo.
- **Parámetros de URL:**
  - `uidb64`: ID del usuario codificado en base64.
  - `token`: Token de verificación.
- **Respuesta:**
  - `200 OK`: `{"message": "Account verified successfully"}`
  - `400 Bad Request`: Si el enlace es inválido o ha expirado.

#### `GET /api/auth/profile/<int:pk>/checkVerified/`
- **Descripción:** Comprueba si un perfil de usuario está verificado.
- **Parámetros de URL:**
  - `pk`: ID del perfil de usuario.
- **Respuesta:**
  - `200 OK`: `{"verified": true/false}`

### Recuperación de Contraseña

#### `POST /api/auth/password/reset/`
- **Descripción:** Inicia el proceso de recuperación de contraseña. Envía un correo con un enlace para restablecerla.
- **Parámetros del Body:**
  - `email` (string, requerido)
- **Respuesta:**
  - `200 OK`: `{"detail": "Password reset e-mail has been sent."}`

#### `POST /api/auth/password/reset/confirm/`
- **Descripción:** Confirma y establece la nueva contraseña.
- **Parámetros del Body:**
  - `uid` (string, requerido)
  - `token` (string, requerido)
  - `password` (string, requerido)
  - `passwordConfirmation` (string, requerido)
- **Respuesta:**
  - `200 OK`: `{"detail": "Password has been reset with the new password."}`
  - `400 Bad Request`: Si los datos son inválidos o las contraseñas no coinciden.
