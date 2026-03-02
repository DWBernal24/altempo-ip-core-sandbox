# Documentación de la Aplicación `services`

Esta aplicación gestiona la taxonomía y la estructura de los servicios ofrecidos en la plataforma.

## Modelos

A continuación se describen los modelos de la base de datos para la aplicación `services`.

### `Tag`

Representa una etiqueta que se puede asociar a las categorías de servicios.

| Campo       | Tipo          | Descripción                               |
|-------------|---------------|-------------------------------------------|
| `name`      | CharField     | Nombre único de la etiqueta (máx. 50).    |
| `description` | TextField     | Descripción opcional (máx. 500).          |

### `Category`

Agrupa diferentes `Item`s de servicio.

| Campo          | Tipo          | Descripción                                       |
|----------------|---------------|---------------------------------------------------|
| `id`           | BigAutoField  | Clave primaria.                                   |
| `name`         | CharField     | Nombre único de la categoría (máx. 100).          |
| `display_name` | CharField     | Nombre para mostrar, único (máx. 100, opcional).  |
| `tag`          | ForeignKey    | Relación con el modelo `Tag`.                     |
| `description`  | TextField     | Descripción opcional (máx. 500).                  |
| `image`        | ImageField    | Imagen opcional para la categoría.                |

### `Item`

Representa un tipo de servicio específico dentro de una `Category`.

| Campo           | Tipo          | Descripción                                                     |
|-----------------|---------------|-----------------------------------------------------------------|
| `id`            | BigAutoField  | Clave primaria.                                                 |
| `name`          | CharField     | Nombre único del item (máx. 150).                               |
| `display_name`  | CharField     | Nombre para mostrar, único (máx. 100, opcional).                |
| `category`      | ForeignKey    | Relación con el modelo `Category`.                              |
| `category_name` | ForeignKey    | Relación con el campo `name` de `Category` (opcional).          |
| `description`   | TextField     | Descripción opcional (máx. 500).                                |
| `image`         | ImageField    | Imagen opcional para el item.                                   |

### `SpecificService`

Define un servicio aún más específico que deriva de un `Item`.

| Campo          | Tipo          | Descripción                                                              |
|----------------|---------------|--------------------------------------------------------------------------|
| `id`           | BigAutoField  | Clave primaria.                                                          |
| `name`         | CharField     | Nombre único del servicio específico (máx. 150).                         |
| `display_name` | CharField     | Nombre para mostrar (máx. 100, opcional).                                |
| `item_name`    | ForeignKey    | Relación con el campo `name` de `Item` (opcional).                       |
| `item`         | ForeignKey    | Relación con el modelo `Item`.                                           |
| `description`  | TextField     | Descripción opcional (máx. 500).                                         |
| `image`        | ImageField    | Imagen opcional para el servicio específico.                             |
| `extra_fields` | JSONField     | Campos adicionales en formato JSON para personalización (opcional).      |

### `ServiceMode`

Define si un servicio es `virtual` o `on_site` (presencial).

| Campo          | Tipo          | Descripción                                       |
|----------------|---------------|---------------------------------------------------|
| `name`         | CharField     | Nombre único del modo (máx. 20).                  |
| `display_name` | CharField     | Nombre para mostrar, único (máx. 100, opcional).  |

### `PricingInterval`

Define los intervalos de precios para los servicios.

| Campo                   | Tipo          | Descripción                                                              |
|-------------------------|---------------|--------------------------------------------------------------------------|
| `duration`              | PositiveIntegerField | Duración del intervalo.                                                  |
| `unit`                  | CharField     | Unidad de tiempo para la duración (e.j., 'horas', 'días').               |
| `price`                 | DecimalField  | Precio del intervalo.                                                    |
| `is_base`               | BooleanField  | Indica si es el precio base (por defecto `False`).                       |
| `music_project_service` | ForeignKey    | Relación con `MusicProjectService` del app `musicians` (opcional).       |

### `Attribute`

Atributos personalizados para un `SpecificService`.

| Campo              | Tipo          | Descripción                                                     |
|--------------------|---------------|-----------------------------------------------------------------|
| `id`               | BigAutoField  | Clave primaria.                                                 |
| `name`             | CharField     | Nombre único del atributo (máx. 100).                           |
| `display_name`     | CharField     | Nombre para mostrar, único (máx. 100, opcional).                |
| `description`      | TextField     | Descripción opcional (máx. 500).                                |
| `specific_service` | ForeignKey    | Relación con el campo `name` de `SpecificService`.              |

---

## API Endpoints

A continuación se detallan los endpoints de la API para la aplicación `services`.

### Tags

-   **`GET /api/services/tags/`**
    -   **Descripción:** Obtiene una lista paginada de todas las etiquetas.
    -   **Respuesta Exitosa (200 OK):**
        ```json
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "name": "Músicos",
                    "description": "Servicios relacionados con músicos"
                }
            ]
        }
        ```

-   **`POST /api/services/tags/`**
    -   **Descripción:** Crea una nueva etiqueta.
    -   **Cuerpo de la Solicitud:**
        ```json
        {
            "name": "Nueva Etiqueta",
            "description": "Descripción de la nueva etiqueta"
        }
        ```
    -   **Respuesta Exitosa (201 Created):** El objeto de la etiqueta creada.

-   **`GET /api/services/tags/<int:pk>/`**
    -   **Descripción:** Obtiene los detalles de una etiqueta específica.
    -   **Respuesta Exitosa (200 OK):** El objeto de la etiqueta.

-   **`PUT /api/services/tags/<int:pk>/`**
    -   **Descripción:** Actualiza una etiqueta existente.
    -   **Respuesta Exitosa (200 OK):** El objeto de la etiqueta actualizada.

-   **`DELETE /api/services/tags/<int:pk>/`**
    -   **Descripción:** Elimina una etiqueta.
    -   **Respuesta Exitosa (204 No Content):** Sin contenido.

### Categories

-   **`GET /api/services/categories/`**
    -   **Descripción:** Obtiene una lista de todas las categorías.
    -   **Respuesta Exitosa (200 OK):** Lista de objetos de categorías.

-   **`POST /api/services/categories/`**
    -   **Descripción:** Crea una nueva categoría.
    -   **Respuesta Exitosa (201 Created):** El objeto de la categoría creada.

-   **`GET /api/services/categories/<int:pk>/`**, **`PUT ...`**, **`DELETE ...`**
    -   **Descripción:** Operaciones CRUD para una categoría específica.

### Items

-   **`GET /api/services/items/`**
    -   **Descripción:** Obtiene una lista de items. Se puede filtrar por categoría.
    -   **Parámetros de Consulta:**
        -   `category` (opcional): ID de la categoría para filtrar los items.
    -   **Ejemplo:** `/api/services/items/?category=1`
    -   **Respuesta Exitosa (200 OK):** Lista de objetos de items.

-   **`POST /api/services/items/`**
    -   **Descripción:** Crea un nuevo item.
    -   **Respuesta Exitosa (201 Created):** El objeto del item creado.

-   **`GET /api/services/items/<int:pk>/`**, **`PUT ...`**, **`DELETE ...`**
    -   **Descripción:** Operaciones CRUD para un item específico.

### Specific Services

-   **`GET /api/services/specific-services/`**
    -   **Descripción:** Obtiene una lista de servicios específicos. Se puede filtrar por item.
    -   **Parámetros de Consulta:**
        -   `item` (opcional): ID del item para filtrar los servicios.
    -   **Ejemplo:** `/api/services/specific-services/?item=2`
    -   **Respuesta Exitosa (200 OK):** Lista de objetos de servicios específicos.

-   **`POST /api/services/specific-services/`**
    -   **Descripción:** Crea un nuevo servicio específico.
    -   **Respuesta Exitosa (201 Created):** El objeto del servicio creado.

-   **`GET /api/services/specific-services/<int:pk>/`**, **`PUT ...`**, **`DELETE ...`**
    -   **Descripción:** Operaciones CRUD para un servicio específico.

### Service Modes

-   **`GET /api/services/service-modes/`**
    -   **Descripción:** Obtiene una lista de todos los modos de servicio (ej. 'virtual', 'on_site').
    -   **Respuesta Exitosa (200 OK):** Lista de objetos de modos de servicio.

-   **`POST /api/services/service-modes/`**
    -   **Descripción:** Crea un nuevo modo de servicio.
    -   **Respuesta Exitosa (201 Created):** El objeto del modo de servicio creado.

-   **`GET /api/services/service-modes/<int:pk>/`**, **`PUT ...`**, **`DELETE ...`**
    -   **Descripción:** Operaciones CRUD para un modo de servicio específico.

### Attributes

-   **`GET /api/services/attributes/`**
    -   **Descripción:** Obtiene una lista de todos los atributos.
    -   **Respuesta Exitosa (200 OK):** Lista de objetos de atributos.

-   **`POST /api/services/attributes/`**
    -   **Descripción:** Crea un nuevo atributo.
    -   **Respuesta Exitosa (201 Created):** El objeto del atributo creado.

-   **`GET /api/services/attributes/<int:pk>/`**, **`PUT ...`**, **`DELETE ...`**
    -   **Descripción:** Operaciones CRUD para un atributo específico.
