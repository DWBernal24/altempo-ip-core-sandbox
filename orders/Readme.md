# Documentación de la Aplicación "orders"

## Modelos

A continuación se describen los modelos de la aplicación `orders`.

### `EventType`

Almacena los tipos de eventos que un cliente puede solicitar.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único del tipo de evento. |
| `description` | `TextField` | Descripción del tipo de evento (opcional). |
| `allow_custom_message` | `BooleanField` | Indica si se permite un mensaje personalizado para este tipo de evento. |
| `image` | `ImageField` | Imagen representativa del tipo de evento (opcional). |
| `sequence` | `IntegerField` | Orden de aparición en las listas. |

### `CustomerLifecycle`

Representa las etapas del ciclo de vida del cliente.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único de la etapa. |
| `description` | `TextField` | Descripción de la etapa (opcional). |

### `EventGoal`

Define los objetivos que un cliente puede tener para un evento.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único del objetivo. |
| `description` | `TextField` | Descripción del objetivo (opcional). |
| `allow_custom_message` | `BooleanField` | Indica si se permite un mensaje personalizado. |
| `customer_lifecycle` | `ForeignKey` | Etapa del ciclo de vida del cliente a la que se asocia este objetivo. |
| `sequence` | `IntegerField` | Orden de aparición. |

### `MusicAmbianceType`

Tipos de ambiente musical para un evento.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único del tipo de ambiente. |
| `image` | `ImageField` | Imagen representativa (opcional). |

### `EventVisit`

Registra las visitas técnicas a un lugar para eventos.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `visit_date` | `DateField` | Fecha de la visita. |
| `visit_time` | `TimeField` | Hora de la visita. |
| `status` | `CharField` | Estado de la visita (`pending`, `visited`, `rejected`). |

### `SoundPackage`

Paquetes de sonido predefinidos.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único del paquete. |
| `description` | `TextField` | Descripción del paquete (opcional). |

### `OrderServiceType`

Tipos de servicio que se pueden incluir en una orden.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único del tipo de servicio. |
| `description` | `TextField` | Descripción (opcional). |
| `image` | `ImageField` | Imagen representativa (opcional). |

### `OrderTemplate`

Plantillas para órdenes pre-configuradas.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `name` | `CharField` | Nombre único de la plantilla. |
| `idea` | `CharField` | Idea principal de la plantilla. |
| `description` | `TextField` | Descripción detallada. |
| `event_type` | `ForeignKey` | Tipo de evento asociado. |
| `duration` | `PositiveIntegerField` | Duración en horas (si es mayor a 4). |
| `modality` | `ForeignKey` | Modalidad del servicio (presencial, virtual). |
| `image` | `ImageField` | Imagen de la plantilla. |
| `ambiance_type` | `ForeignKey` | Tipo de ambiente musical. |
| `music_genre_tags` | `ManyToManyField` | Géneros musicales asociados. |
| `instruments` | `ManyToManyField` | Instrumentos incluidos. |
| `technical_level` | `CharField` | Nivel técnico requerido (`medium`, `proffesional`). |
| `logistics` | `BooleanField` | Indica si incluye logística. |
| `personalization` | `TextField` | Opciones de personalización. |
| `price` | `FloatField` | Precio de la plantilla. |
| `featured_tag` | `CharField` | Etiqueta destacada (`popular`, `new`, etc.). |
| `cta_label_1` | `CharField` | Etiqueta para el primer llamado a la acción. |
| `cta_label_2` | `CharField` | Etiqueta para el segundo llamado a la acción. |

### `Order`

Modelo principal que representa una orden de servicio.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `order_number` | `CharField` | Número único de la orden (generado automáticamente). |
| `order_template` | `ForeignKey` | Plantilla de orden utilizada (opcional). |
| `event_type` | `ForeignKey` | Tipo de evento. |
| `event_type_custom_message` | `TextField` | Mensaje personalizado para el tipo de evento. |
| `event_goal` | `ForeignKey` | Objetivo del evento. |
| `event_goal_custom_message` | `TextField` | Mensaje personalizado para el objetivo del evento. |
| `ambiance_type` | `ForeignKey` | Tipo de ambiente musical. |
| `music_genre_tags` | `ManyToManyField` | Géneros musicales. |
| `status` | `CharField` | Estado actual de la orden. |
| `has_specific_requirements` | `BooleanField` | Indica si hay requisitos específicos. |
| `specific_requirements` | `TextField` | Descripción de los requisitos específicos. |
| `estimated_age` | `IntegerField` | Edad estimada del público. |
| `profile_beneficiary` | `TextField` | Perfil del beneficiario del evento. |
| `service_type` | `ForeignKey` | Tipo de servicio principal. |
| `item` | `ForeignKey` | Ítem principal de la orden. |
| `collab_type` | `ForeignKey` | Tipo de colaboración. |
| `modality` | `ForeignKey` | Modalidad del evento (presencial/virtual). |
| `event_city` | `TextField` | Ciudad del evento. |
| `event_address` | `TextField` | Dirección del evento. |
| `latitude` | `DecimalField` | Latitud de la ubicación. |
| `longitude` | `DecimalField` | Longitud de la ubicación. |
| `venue_type` | `CharField` | Tipo de lugar (`indoor`/`outdoor`). |
| `path` | `CharField` | Camino de creación de la orden (`blank`, `artist`, `template`, etc.). |
| `category` | `CharField` | Categoría de la orden (`onlyMusic`, `complete`, etc.). |
| `sound_setup` | `CharField` | Configuración de sonido. |
| `estimated_capacity` | `CharField` | Capacidad estimada del evento. |
| `visit` | `ForeignKey` | Visita técnica asociada (si es necesaria). |
| `sound_restriction` | `BooleanField` | Indica si hay restricciones de sonido. |
| `sound_package` | `ForeignKey` | Paquete de sonido seleccionado. |
| `event_date` | `DateField` | Fecha del evento. |
| `event_duration` | `CharField` | Duración del evento. |
| `custom_duration` | `PositiveIntegerField` | Duración personalizada en horas. |
| `referral_source` | `ForeignKey` | Fuente de referencia del cliente. |
| `additional_comments` | `TextField` | Comentarios adicionales. |
| `user_profile` | `ForeignKey` | Perfil de usuario que creó la orden. |
| `list_musicprojects` | `ManyToManyField` | Proyectos musicales seleccionados. |
| `categories_music` | `ManyToManyField` | Categorías musicales seleccionadas. |
| `list_equipment` | `ManyToManyField` | Equipos seleccionados. |
| `ideas_requirements` | `TextField` | Ideas y requerimientos del cliente. |
| `min_budget` | `DecimalField` | Presupuesto mínimo. |
| `max_budget` | `DecimalField` | Presupuesto máximo. |

### `OrderItem`

Representa un ítem específico dentro de una orden.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `order` | `ForeignKey` | Orden a la que pertenece el ítem. |
| `specific_service` | `ForeignKey` | Servicio específico del ítem. |
| `attribute` | `ForeignKey` | Atributo del servicio. |
| `quantity` | `PositiveIntegerField` | Cantidad. |
| `instruments` | `ManyToManyField` | Instrumentos asociados. |
| `musician_voice_type` | `ForeignKey` | Tipo de voz del músico. |
| `vocal_style` | `ForeignKey` | Estilo vocal. |
| `dj_type` | `ForeignKey` | Tipo de DJ. |
| `category_music` | `ForeignKey` | Categoría musical. |

### `AdditionalEquipment`

Equipo adicional requerido para una orden.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `order` | `ForeignKey` | Orden a la que pertenece el equipo. |
| `equipment` | `ForeignKey` | Equipo específico. |
| `quantity` | `PositiveIntegerField` | Cantidad. |

---

## Endpoints de la API

A continuación se detallan los endpoints disponibles en la aplicación `orders`.

### Eventos y Opciones

- **`GET /api/orders/event-types/`**
  - **Descripción:** Obtiene la lista de tipos de eventos (ocasiones).
  - **Respuesta:** Lista paginada de objetos `EventType`.

- **`GET /api/orders/customer-lifecycles/`**
  - **Descripción:** Obtiene la lista de ciclos de vida del cliente.
  - **Respuesta:** Lista paginada de objetos `CustomerLifecycle`.

- **`GET /api/orders/event-goals/`**
  - **Descripción:** Obtiene la lista de objetivos de eventos.
  - **Parámetros (Query):** `customer_lifecycle` (ID) para filtrar por ciclo de vida.
  - **Respuesta:** Lista paginada de objetos `EventGoal`.

- **`GET /api/orders/music-ambience-types/`**
  - **Descripción:** Obtiene los tipos de ambiente musical.
  - **Respuesta:** Lista paginada de objetos `MusicAmbianceType`.

- **`GET /api/orders/service-types/`**
  - **Descripción:** Obtiene los tipos de servicios para una orden.
  - **Respuesta:** Lista paginada de objetos `OrderServiceType`.

- **`GET /api/orders/sound-packages/`**
  - **Descripción:** Obtiene los paquetes de sonido disponibles.
  - **Respuesta:** Lista paginada de objetos `SoundPackage`.

- **`GET /api/orders/templates/`**
  - **Descripción:** Obtiene la lista de plantillas de órdenes.
  - **Respuesta:** Lista paginada de objetos `OrderTemplate`.

### Órdenes (Orders)

- **`POST /api/orders/`**
  - **Descripción:** Crea una nueva orden. Requiere autenticación.
  - **Cuerpo (Body):** Objeto `OrderSerializer` con los datos de la nueva orden.
  - **Respuesta:**
    ```json
    {
      "message": "Order created successfully!",
      "order_id": "ORD-YYYYMMDD-XXXXX"
    }
    ```

- **`GET /api/orders/`**
  - **Descripción:** Obtiene la lista de órdenes del usuario autenticado.
  - **Respuesta:** Lista paginada de objetos `OrderListLevelOneSerializer`.

- **`GET /api/orders/<id>/`**
  - **Descripción:** Obtiene el detalle de una orden específica por su `order_number`. Requiere autenticación.
  - **Respuesta:** Objeto `OrderListSerializer` con el detalle completo de la orden.

- **`PUT /api/orders/<id>/`**
  - **Descripción:** Cancela una orden específica. El `id` corresponde al `order_number`. Requiere autenticación.
  - **Cuerpo (Body):** Vacío.
  - **Respuesta:** Objeto `OrderListSerializer` de la orden cancelada.

- **`PUT /api/ordersupdate/`**
  - **Descripción:** Actualiza una orden existente. Requiere autenticación.
  - **Cuerpo (Body):** Objeto `OrderUpdateSerializer` con los campos a modificar, incluyendo `order_number`.
  - **Respuesta:**
    ```json
    {
      "message": "Exitoso"
    }
    ```

- **`GET /api/orders/active/list`**
  - **Descripción:** Obtiene una lista de las órdenes activas del usuario autenticado.
  - **Respuesta:** Lista paginada de objetos `OrderListLevelOneSerializer`.

- **`GET /api/orders/active/count`**
  - **Descripción:** Obtiene la cantidad de órdenes activas del usuario autenticado.
  - **Respuesta:**
    ```json
    {
      "active_orders_count": 5
    }
    ```

- **`GET /api/orders/by-category`**
  - **Descripción:** Obtiene las órdenes del usuario filtradas por categoría.
  - **Parámetros (Query):** `category` (string).
  - **Respuesta:** Lista paginada de objetos `OrderListLevelOneSerializer`.

- **`GET /api/orders/nearest`**
  - **Descripción:** Obtiene la orden (futura o pasada) más cercana a la fecha actual para el usuario autenticado.
  - **Respuesta:** Objeto `OrderListSerializer` de la orden más cercana.

### Ítems de la Orden (Order Items)

- **`GET /api/orderitems/list`**
  - **Descripción:** Obtiene los ítems de una orden específica.
  - **Parámetros (Query):** `order` (el `order_number` de la orden).
  - **Respuesta:** Lista paginada de objetos `OrderItemListSerializer`.

### Administración de Órdenes

- **`GET /api/orders-admin/`**
  - **Descripción:** Obtiene una lista de todas las órdenes en el sistema (para administradores). Requiere autenticación y permisos de administrador.
  - **Respuesta:** Lista paginada de objetos `OrderListLevelOneSerializer`.

- **`PUT /api/orders-admin/`**
  - **Descripción:** Permite a un administrador actualizar el estado de una orden.
  - **Cuerpo (Body):**
    ```json
    {
      "order_number": "ORD-YYYYMMDD-XXXXX",
      "status": "NEW_STATUS"
    }
    ```
  - **Respuesta:**
    ```json
    {
      "message": "Exitoso"
    }
    ```
