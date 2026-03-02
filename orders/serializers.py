from rest_framework import serializers
from orders.models import (
    EventType,
    CustomerLifecycle,
    EventGoal,
    MusicAmbianceType,
    Order,
    OrderItem,
    EventVisit,
    AdditionalEquipment,
    OrderServiceType,
    SoundPackage, OrderTemplate,
)
from services.models import SpecificService
from roles.models import UserProfile
from core.models import MusicalGenreTag, Instrument, MusicianVoiceType, VocalStyle, Equipment, DJType
from musicians.models import MusicProject, CategoryMusic

def asignCategory(data):
    path = data.get('path')
    list_equipment = data.get('data_equipments')
    if list_equipment and len(list_equipment) > 0 and path == 'artist':
        return 'complete'
    if path == 'band' or path == 'template':
        return 'complementary'
    if path == 'artist' or path == 'band':
        return 'onlyMusic'
    if path == 'onlyMusic':
        return 'onlyEquipment'
    return None


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class CustomerLifecycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerLifecycle
        fields = '__all__'


class EventGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventGoal
        fields = '__all__'


class MusicAmbianceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MusicAmbianceType
        fields = '__all__'

class OrderServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderServiceType
        fields = '__all__'

class OrderTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderTemplate
        fields = '__all__'


class SoundPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoundPackage
        fields = '__all__'


class EventVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventVisit
        fields = ['visit_date', 'visit_time']


class OrderItemBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    instruments = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    specific_service = serializers.PrimaryKeyRelatedField(
        queryset=SpecificService.objects.all()
    )
    musician_voice_type = serializers.PrimaryKeyRelatedField(
        queryset=MusicianVoiceType.objects.all(), required=False
    )
    vocal_style = serializers.PrimaryKeyRelatedField(
        queryset=VocalStyle.objects.all(), required=False
    )

    class Meta:
        model = OrderItem
        fields = [
            "specific_service", "attribute", "quantity", "instruments",
            "musician_voice_type", "vocal_style", "dj_type"
        ]

    def validate(self, data):
        data = super().validate(data)

        # Get specific servie
        specific_service = data.get("specific_service")

        # Validate extra fields
        extra_fields = specific_service.extra_fields.get("extra_fields", [])

        for extra_field in extra_fields:
            field_key = extra_field["field_key"]

            if not data.get(field_key):
                raise serializers.ValidationError(f"{field_key} is mandatory")

        return data

    def create(self, validated_data):
        instruments_data = validated_data.pop("instruments", [])
        order_item = OrderItem.objects.create(**validated_data)

        if instruments_data:
            instruments = Instrument.objects.filter(id__in=instruments_data)
            order_item.instruments.set(instruments)

        return order_item

class OrderItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        depth = 2

class AdditionalEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalEquipment
        fields = ['equipment', 'quantity']


class OrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 2

class OrderListLevelOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "event_type_custom_message",
            "event_goal_custom_message",
            "status",
            "specific_requirements",
            "estimated_age",
            "profile_beneficiary",
            "event_city",
            "event_address",
            "venue_type",
            "path",
            "sound_setup",
            "estimated_capacity",
            "event_date",
            "event_duration",
            "custom_duration",
            "event_type",
        ]
        depth = 1


class OrderSerializer(serializers.ModelSerializer):

    """
        Este debe contener los siguientes campos para el primer camino de crear una orden en blanco:
            1. event_type: Que proviene de la tabla de EventType de una pagina de tipo de ocasión, blank, artist
            2. No va. customer_life_cycle: Que probiene de la tabla CustomerLifecycle que proviene de la sección areas y perfiles, blank
            3. event_goal: Este proviene de la tabla EventGoal que proviene en la sección de cambia tus objetivos, blank
            4. ambiance_type: Este proviene de la tabla EventAtmosphere (Se debe crear los get correspondientes), blank
            5. musician_ambience_type: Este proviene de la tabla MusicAmbianceType, blank
            6. music_genre_tag: Este proviene de la tabla MusicalGenreTag Este es una lista, blank, artist, band
            7. has_specific_requirements: Campo booleano, blank
            8. specific_requirements: campo de texto, blank
            9. reference: campo de texto, blank
            10. in_person: campo booleano, blank, artist
            11. address: Direccion ingresada por el usuario, blank, template, artist, band
            12. city: Ciudad ingresada por el usuario, blank, template, artist, band
            13. latitude: Latitud de la direccion, blank, template, artist, band
            14. lontiguted: Longited de la dirección, blank, template, artist, band
            15. outdoors: campo booleano, blank, template, artist, band
            16. sound_equipment: Este proviene de la tabla SoundEquipment (crear el modelo), blank, template, artist, band
            17. capacity_estimated: Este proviene de la tabla CapacityEstimated (Crear el modelo), blank, template, artist, band
            18. visit_date: campo fecha de la visita, blank, template, artist, band
            19. visit_hour: Campo de hora de la visita, blank, template, artist, band
            20. have_sound_restriction: campo booleano, blank, template, artist, band
            21. equipment_list: Este es una lista y proviene de la tabla Equipment, blank, template, artist, band
            22. duration_event: Proviene de la tabla Duration_event (creación del modelo), blank, template, artist, band
            23. path: Este es un campo de texto: donde puede ser template, blank, artist y band.
            24. template: Este proviene de la tabla TemplateOrder (crear modelo), template
            25. musician: proviene de la tabla User, este tiene que ser músico. Esto es una lista, artist
            26. additional_services: Servicios adicionales que proviene de la tabla OrderServiceType, artist
            27. max_budget: Campo numerico para saber el presupuesto de la tabla. artist
            29. band: Este proviene de la tabla de MusicianProject. band
            30. type_collaboration: tipo de colaboración que buscas, proviene de la tabla CollabType. band
            31. profile_musician: Lista de artistas que se necesita. Proviene de la tabla de ProfileMusician. band
            32. min_budget: Campo numero del presupuesto. artist

    """

    music_genre_tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    list_musicprojects = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    order_items = OrderItemBasicSerializer(many=True, write_only=True, required=False)
    visit = EventVisitSerializer(write_only=True, many=False, required=False)
    additional_equipment = AdditionalEquipmentSerializer(many=True, write_only=True, required=False)
    user = serializers.IntegerField(required=True, write_only=True)
    path = serializers.CharField(required=True)
    categories_music_list = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    data_equipments = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'event_type', 'event_type_custom_message', 'event_goal', 'event_goal_custom_message', 'ambiance_type',
            'music_genre_tags', 'has_specific_requirements', 'service_type', 'item', 'order_items', 'collab_type',
            'modality', 'event_city', 'visit', 'additional_equipment', 'event_address', 'latitude', 'longitude',
            'venue_type', 'sound_setup', 'estimated_capacity', 'sound_restriction', 'sound_package', 'event_date',
            'event_duration', 'custom_duration', 'referral_source', 'additional_comments', 'specific_requirements',
            'user', 'min_budget', 'max_budget', 'path', 'estimated_age', 'profile_beneficiary', 'order_template',
            'list_musicprojects', 'categories_music_list', 'data_equipments', 'ideas_requirements'
        ]


    def validate(self, data):
        data = super().validate(data)

        event_type = data.get('event_type')
        event_type_custom_message = data.get("event_type_custom_message")
        ambiance_type = data.get("ambiance_type")
        music_genre_tags = data.get("music_genre_tags")
        event_goal = data.get('event_goal')
        has_specific_requirements = data.get('has_specific_requirements', False)
        estimated_age = data.get("estimated_age")
        profile_beneficiary = data.get("profile_beneficiary")
        modality = data.get("modality")
        event_city = data.get("event_city")
        event_address = data.get("event_address")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        venue_type = data.get("venue_type")
        sound_setup = data.get("sound_setup")
        estimated_capacity = data.get("estimated_capacity")

        estimated_capacity = data.get('estimated_capacity', None)
        event_duration = data.get('event_duration')
        path = data.get('path')
        order_template = data.get('order_template')
        list_artist = data.get('list_musicprojects')
        categories_music = data.get('categories_music_list')
        list_equipments = data.get('data_equipments')


        if path == "blank":
            # validando para saber si el usuario escogio otro y que ingrese el evento
            if event_type.allow_custom_message and not event_type_custom_message:
                raise serializers.ValidationError("Event type requires a custom message.")
            # validando los objetivos de la orden de compra
            if event_goal.allow_custom_message and not data.get("event_goal_custom_message"):
                raise serializers.ValidationError("Event goal requires a custom message.")
            # validando el ambiente requerido
            if not ambiance_type:
                raise serializers.ValidationError("El ambiente es requerido")
            # validando el tipo de musica
            if not music_genre_tags and len(music_genre_tags) == 0:
                raise serializers.ValidationError("Los generos musicales son requeridos")
            # validando los requesitos
            if has_specific_requirements and not data.get("specific_requirements"):
                raise serializers.ValidationError("Specific requirements requires a description.")
            # validando la edad
            if not estimated_age:
                raise serializers.ValidationError("La edad estimada es requerida")
            if not modality:
                raise serializers.ValidationError("La modalidad es requerida")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")

        if path == 'template':
            if not estimated_age:
                raise serializers.ValidationError("La edad estimada es requerida")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")
            if not order_template:
                raise serializers.ValidationError("order_template es requerido")

        if path == 'artist':
            # validando para saber si el usuario escogio otro y que ingrese el evento
            if event_type.allow_custom_message and not event_type_custom_message:
                raise serializers.ValidationError("Event type requires a custom message.")
            # validando los objetivos de la orden de compra
            if event_goal.allow_custom_message and not data.get("event_goal_custom_message"):
                raise serializers.ValidationError("Event goal requires a custom message.")
            if not estimated_age:
                raise serializers.ValidationError("La edad estimada es requerida")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")
            if not categories_music:
                raise serializers.ValidationError("categories_music_list e es requerido")

        if path == 'band':
            # validando el tipo de musica
            if not music_genre_tags and len(music_genre_tags) == 0:
                raise serializers.ValidationError("Los generos musicales son requeridos")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")

        if path == 'onlyMusic':
            if not list_equipments and len(list_equipments) == 0:
                raise serializers.ValidationError("Lista de equipo de sonido es requerido")

        return data

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        order_items_data = validated_data.pop("order_items", [])
        event_visit = validated_data.pop("visit", None)
        additional_equipment = validated_data.pop("additional_equipment", {})


        user_profile = UserProfile.objects.get(user__id=user_id)

        # Create Order Visit if it's necessary
        visit_obj = None

        if event_visit:
            visit_serializer = EventVisitSerializer(data=event_visit)
            visit_serializer.is_valid(raise_exception=True)
            visit_obj = visit_serializer.save()


        # Create order
        order = Order.objects.create(
            user_profile=user_profile,
            path=validated_data.get("path"),
            order_template=validated_data.get("order_template"),
            event_type=validated_data.get("event_type"),
            event_type_custom_message= validated_data.get("event_type_custom_message", None),
            event_goal=validated_data.get("event_goal"),
            event_goal_custom_message=validated_data.get("event_goal_custom_message", None),
            ambiance_type=validated_data.get("ambiance_type"),
            has_specific_requirements=validated_data.get('has_specific_requirements', False),
            specific_requirements=validated_data.get('specific_requirements', None),
            service_type=validated_data.get("service_type"),
            item=validated_data.get("item"),
            collab_type=validated_data.get("collab_type"),
            modality=validated_data.get("modality"),
            event_city=validated_data.get("event_city"),
            event_address=validated_data.get("event_address"),
            latitude=validated_data.get("latitude"),
            longitude=validated_data.get("longitude"),
            venue_type=validated_data.get("venue_type"),
            sound_setup=validated_data.get("sound_setup"),
            estimated_capacity=validated_data.get("estimated_capacity"),
            visit=visit_obj if visit_obj else None,
            sound_restriction=validated_data.get("sound_restriction"),
            sound_package=validated_data.get("sound_package", None),
            event_date=validated_data.get("event_date"),
            event_duration=validated_data.get("event_duration"),
            custom_duration=validated_data.get("custom_duration", None),
            referral_source=validated_data.get("referral_source", None),
            additional_comments=validated_data.get("additional_comments", None),
            max_budget=validated_data.get("max_budget", None),
            min_budget=validated_data.get("min_budget", None),
            estimated_age=validated_data.get("estimated_age"),
            category=asignCategory(validated_data),
            ideas_requirements=validated_data.get("ideas_requirements", None)
        )

        # Adding music genres
        music_genre_tags = validated_data.get("music_genre_tags", [])

        if music_genre_tags:
            genre_tags = MusicalGenreTag.objects.filter(id__in=music_genre_tags)
            order.music_genre_tags.set(genre_tags)

        # Adding music genres
        list_artist = validated_data.get("list_musicprojects", [])

        if list_artist:
            artist = MusicProject.objects.filter(id__in=list_artist)
            order.list_musicprojects.set(artist)

        #adding categories music
        categories_music = validated_data.get('categories_music_list', [])
        if categories_music:
            category = CategoryMusic.objects.filter(id__in=categories_music)
            order.categories_music.set(category)

        list_equipments = validated_data.get('data_equipments',  [])
        if list_equipments:
            equipments = Equipment.objects.filter(id__in=list_equipments)
            order.list_equipment.set(equipments)

        # Order Items logic
        if order_items_data:
            for item in order_items_data:
                if isinstance(item.get("specific_service"), SpecificService):
                    item["specific_service"] = item["specific_service"].id

                if isinstance(item.get("musician_voice_type"), MusicianVoiceType):
                    item["musician_voice_type"] = item["musician_voice_type"].id

                if isinstance(item.get("vocal_style"), VocalStyle):
                    item["vocal_style"] = item["vocal_style"].id

                if isinstance(item.get("dj_type"), DJType):
                    item["dj_type"] = item["dj_type"].id

                if isinstance(item.get('category_music'), CategoryMusic):
                    item["category_music"] = item["category_music"].id

                instruments = item.get("instruments")
                if instruments and len(instruments) > 0:
                    ids = []
                    for inst in instruments:
                        # acepta instancias o ids
                        if hasattr(inst, "id"):
                            ids.append(inst.id)
                        else:
                            ids.append(int(inst))
                    item["instruments"] = ids

        order_item_serializer = OrderItemBasicSerializer(data=order_items_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)
        order_item_serializer.save(order=order)

        # Additional equipment
        if additional_equipment:
            for item in additional_equipment:
                if isinstance(item['equipment'], Equipment):
                    item['equipment'] = item["equipment"].id
            additional_equipment_serializer = AdditionalEquipmentSerializer(data=additional_equipment, many=True)
            additional_equipment_serializer.is_valid(raise_exception=True)
            additional_equipment_serializer.save(order=order)

        return order

class OrderUpdateOnlyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderUpdateSerializer(serializers.ModelSerializer):

    """
        Este debe contener los siguientes campos para el primer camino de crear una orden en blanco:
            1. event_type: Que proviene de la tabla de EventType de una pagina de tipo de ocasión, blank, artist
            2. No va. customer_life_cycle: Que probiene de la tabla CustomerLifecycle que proviene de la sección areas y perfiles, blank
            3. event_goal: Este proviene de la tabla EventGoal que proviene en la sección de cambia tus objetivos, blank
            4. ambiance_type: Este proviene de la tabla EventAtmosphere (Se debe crear los get correspondientes), blank
            5. musician_ambience_type: Este proviene de la tabla MusicAmbianceType, blank
            6. music_genre_tag: Este proviene de la tabla MusicalGenreTag Este es una lista, blank, artist, band
            7. has_specific_requirements: Campo booleano, blank
            8. specific_requirements: campo de texto, blank
            9. reference: campo de texto, blank
            10. in_person: campo booleano, blank, artist
            11. address: Direccion ingresada por el usuario, blank, template, artist, band
            12. city: Ciudad ingresada por el usuario, blank, template, artist, band
            13. latitude: Latitud de la direccion, blank, template, artist, band
            14. lontiguted: Longited de la dirección, blank, template, artist, band
            15. outdoors: campo booleano, blank, template, artist, band
            16. sound_equipment: Este proviene de la tabla SoundEquipment (crear el modelo), blank, template, artist, band
            17. capacity_estimated: Este proviene de la tabla CapacityEstimated (Crear el modelo), blank, template, artist, band
            18. visit_date: campo fecha de la visita, blank, template, artist, band
            19. visit_hour: Campo de hora de la visita, blank, template, artist, band
            20. have_sound_restriction: campo booleano, blank, template, artist, band
            21. equipment_list: Este es una lista y proviene de la tabla Equipment, blank, template, artist, band
            22. duration_event: Proviene de la tabla Duration_event (creación del modelo), blank, template, artist, band
            23. path: Este es un campo de texto: donde puede ser template, blank, artist y band.
            24. template: Este proviene de la tabla TemplateOrder (crear modelo), template
            25. musician: proviene de la tabla User, este tiene que ser músico. Esto es una lista, artist
            26. additional_services: Servicios adicionales que proviene de la tabla OrderServiceType, artist
            27. max_budget: Campo numerico para saber el presupuesto de la tabla. artist
            29. band: Este proviene de la tabla de MusicianProject. band
            30. type_collaboration: tipo de colaboración que buscas, proviene de la tabla CollabType. band
            31. profile_musician: Lista de artistas que se necesita. Proviene de la tabla de ProfileMusician. band
            32. min_budget: Campo numero del presupuesto. artist

    """

    music_genre_tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    list_musicprojects = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    order_items = OrderItemSerializer(many=True, write_only=True, required=False)
    visit = EventVisitSerializer(write_only=True, many=False, required=False)
    additional_equipment = AdditionalEquipmentSerializer(many=True, write_only=True, required=False)
    user = serializers.IntegerField(required=True, write_only=True)
    path = serializers.CharField(required=True)
    categories_music_list = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    data_equipments = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'event_type', 'event_type_custom_message', 'event_goal', 'event_goal_custom_message', 'ambiance_type',
            'music_genre_tags', 'has_specific_requirements', 'service_type', 'item', 'order_items', 'collab_type',
            'modality', 'event_city', 'visit', 'additional_equipment', 'event_address', 'latitude', 'longitude',
            'venue_type', 'sound_setup', 'estimated_capacity', 'sound_restriction', 'sound_package', 'event_date',
            'event_duration', 'custom_duration', 'referral_source', 'additional_comments', 'specific_requirements',
            'user', 'min_budget', 'max_budget', 'path', 'estimated_age', 'profile_beneficiary', 'order_template',
            'list_musicprojects', 'categories_music_list', 'data_equipments', 'ideas_requirements', 'order_number'
        ]


    def validate(self, data):
        data = super().validate(data)

        event_type = data.get('event_type')
        event_type_custom_message = data.get("event_type_custom_message")
        ambiance_type = data.get("ambiance_type")
        music_genre_tags = data.get("music_genre_tags")
        event_goal = data.get('event_goal')
        has_specific_requirements = data.get('has_specific_requirements', False)
        estimated_age = data.get("estimated_age")
        modality = data.get("modality")
        event_city = data.get("event_city")
        event_address = data.get("event_address")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        venue_type = data.get("venue_type")
        sound_setup = data.get("sound_setup")
        estimated_capacity = data.get("estimated_capacity")

        estimated_capacity = data.get('estimated_capacity', None)
        event_duration = data.get('event_duration')
        path = data.get('path')
        order_template = data.get('order_template')
        categories_music = data.get('categories_music_list')
        list_equipments = data.get('data_equipments')
        order_number = data.get('order_number')

        if not order_number:
            raise serializers.ValidationError("Numero de orden no definido.")

        if path == "blank":
            # validando para saber si el usuario escogio otro y que ingrese el evento
            if event_type.allow_custom_message and not event_type_custom_message:
                raise serializers.ValidationError("Event type requires a custom message.")
            # validando los objetivos de la orden de compra
            if event_goal.allow_custom_message and not data.get("event_goal_custom_message"):
                raise serializers.ValidationError("Event goal requires a custom message.")
            # validando el ambiente requerido
            if not ambiance_type:
                raise serializers.ValidationError("El ambiente es requerido")
            # validando el tipo de musica
            if not music_genre_tags and len(music_genre_tags) == 0:
                raise serializers.ValidationError("Los generos musicales son requeridos")
            # validando los requesitos
            if has_specific_requirements and not data.get("specific_requirements"):
                raise serializers.ValidationError("Specific requirements requires a description.")
            # validando la edad
            if not estimated_age:
                raise serializers.ValidationError("La edad estimada es requerida")
            if not modality:
                raise serializers.ValidationError("La modalidad es requerida")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")

        if path == 'template':
            if not estimated_age:
                raise serializers.ValidationError("La edad estimada es requerida")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")
            if not order_template:
                raise serializers.ValidationError("order_template es requerido")

        if path == 'artist':
            # validando para saber si el usuario escogio otro y que ingrese el evento
            if event_type.allow_custom_message and not event_type_custom_message:
                raise serializers.ValidationError("Event type requires a custom message.")
            # validando los objetivos de la orden de compra
            if event_goal.allow_custom_message and not data.get("event_goal_custom_message"):
                raise serializers.ValidationError("Event goal requires a custom message.")
            if not estimated_age:
                raise serializers.ValidationError("La edad estimada es requerida")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")
            if not categories_music:
                raise serializers.ValidationError("categories_music_list e es requerido")

        if path == 'band':
            # validando el tipo de musica
            if not music_genre_tags and len(music_genre_tags) == 0:
                raise serializers.ValidationError("Los generos musicales son requeridos")
            if not event_city:
                raise serializers.ValidationError("La ciudad es requerida")
            if not event_address:
                raise serializers.ValidationError("La dirección es requerida")
            if not latitude and not longitude:
                raise serializers.ValidationError("La latitud y longitud es requerida")
            if not venue_type:
                raise serializers.ValidationError("La modalidad es requerida")
            if not sound_setup:
                raise serializers.ValidationError("Equipo de montaje es requerido")
            if not estimated_capacity:
                raise serializers.ValidationError("Aforo estimado es requerido")
            if event_duration == "custom" and not data.get("custom_duration"):
                raise serializers.ValidationError("For more than4 hours , the custom duration is mandatory.")

        if path == 'onlyMusic':
            if not list_equipments and len(list_equipments) == 0:
                raise serializers.ValidationError("Lista de equipo de sonido es requerido")

        return data

    def update(self, order, validated_data):
        user_id = validated_data.pop("user")
        order_items_data = validated_data.pop("order_items", [])
        event_visit = validated_data.pop("visit", None)
        additional_equipment = validated_data.pop("additional_equipment", {})


        user_profile = UserProfile.objects.get(user__id=user_id)

        # Create Order Visit if it's necessary
        visit_obj = None

        if event_visit:
            visit_serializer = EventVisitSerializer(data=event_visit)
            visit_serializer.is_valid(raise_exception=True)
            visit_obj = visit_serializer.save()

        order.path = validated_data.get("path")
        order.order_template=validated_data.get("order_template")
        order.event_type=validated_data.get("event_type")
        order.event_type_custom_message= validated_data.get("event_type_custom_message", None)
        order.event_goal=validated_data.get("event_goal")
        order.event_goal_custom_message=validated_data.get("event_goal_custom_message", None)
        order.ambiance_type=validated_data.get("ambiance_type")
        order.has_specific_requirements=validated_data.get('has_specific_requirements', False)
        order.specific_requirements=validated_data.get('specific_requirements', None)
        order.service_type=validated_data.get("service_type")
        order.item=validated_data.get("item")
        order.collab_type=validated_data.get("collab_type")
        order.modality=validated_data.get("modality")
        order.event_city=validated_data.get("event_city")
        order.event_address=validated_data.get("event_address")
        order.latitude=validated_data.get("latitude")
        order.longitude=validated_data.get("longitude")
        order.venue_type=validated_data.get("venue_type")
        order.sound_setup=validated_data.get("sound_setup")
        order.estimated_capacity=validated_data.get("estimated_capacity")
        order.visit=visit_obj if visit_obj else None
        order.sound_restriction=validated_data.get("sound_restriction")
        order.sound_package=validated_data.get("sound_package", None)
        order.event_date=validated_data.get("event_date")
        order.event_duration=validated_data.get("event_duration")
        order.custom_duration=validated_data.get("custom_duration", None)
        order.referral_source=validated_data.get("referral_source", None)
        order.additional_comments=validated_data.get("additional_comments", None)
        order.max_budget=validated_data.get("max_budget", None)
        order.min_budget=validated_data.get("min_budget", None)
        order.estimated_age=validated_data.get("estimated_age")
        order.category=asignCategory(validated_data)
        order.ideas_requirements=validated_data.get("ideas_requirements", None)

        # Adding music genres
        music_genre_tags = validated_data.get("music_genre_tags", [])

        if music_genre_tags:
            genre_tags = MusicalGenreTag.objects.filter(id__in=music_genre_tags)
            order.music_genre_tags.set(genre_tags)

        # Adding music genres
        list_artist = validated_data.get("list_musicprojects", [])

        if list_artist:
            artist = MusicProject.objects.filter(id__in=list_artist)
            order.list_musicprojects.set(artist)

        #adding categories music
        categories_music = validated_data.get('categories_music_list', [])
        if categories_music:
            category = CategoryMusic.objects.filter(id__in=categories_music)
            order.categories_music.set(category)

        list_equipments = validated_data.get('data_equipments',  [])
        if list_equipments:
            equipments = Equipment.objects.filter(id__in=list_equipments)
            order.list_equipment.set(equipments)

        # Order Items logic
        if order_items_data:
            for item in order_items_data:
                if isinstance(item.get("specific_service"), SpecificService):
                    item["specific_service"] = item["specific_service"].id

                if isinstance(item.get("musician_voice_type"), MusicianVoiceType):
                    item["musician_voice_type"] = item["musician_voice_type"].id

                if isinstance(item.get("vocal_style"), VocalStyle):
                    item["vocal_style"] = item["vocal_style"].id

                if isinstance(item.get("dj_type"), DJType):
                    item["dj_type"] = item["dj_type"].id

                if isinstance(item.get('category_music'), CategoryMusic):
                    item["category_music"] = item=["category_music"].id

                if len(item.get('instruments')) > 0:
                    instruments = item.get("instruments")
                    ids = []
                    for inst in instruments:
                        # acepta instancias o ids
                        if hasattr(inst, "id"):
                            ids.append(inst.id)
                        else:
                            ids.append(int(inst))
                    item["instruments"] = ids

        order_item_serializer = OrderItemBasicSerializer(data=order_items_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)
        order_item_serializer.save(order=order)

        # Additional equipment
        if additional_equipment:
            for item in additional_equipment:
                if isinstance(item['equipment'], Equipment):
                    item['equipment'] = item["equipment"].id
            additional_equipment_serializer = AdditionalEquipmentSerializer(data=additional_equipment, many=True)
            additional_equipment_serializer.is_valid(raise_exception=True)
            additional_equipment_serializer.save(order=order)

        order.save()
        return order

