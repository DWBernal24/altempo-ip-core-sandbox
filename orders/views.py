from os import environ
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers, views, response, status
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from utils.email import send_template_email
from roles.models import (
    UserProfile
)
from orders.models import (
    EventType, CustomerLifecycle, EventGoal, MusicAmbianceType,
    OrderServiceType, SoundPackage, OrderTemplate, Order, OrderItem
)
from orders.serializers import (
    EventTypeSerializer,
    CustomerLifecycleSerializer,
    EventGoalSerializer,
    MusicAmbianceTypeSerializer,
    OrderSerializer,
    OrderServiceTypeSerializer,
    SoundPackageSerializer,
    OrderTemplateSerializer,
    OrderModelSerializer,
    OrderListSerializer,
    OrderListLevelOneSerializer,
    OrderItemListSerializer,
    OrderUpdateSerializer,
    OrderUpdateOnlyStatusSerializer,
)


class EventTypeListView(views.APIView):
    model = EventType
    serializer_class = EventTypeSerializer

    @extend_schema(
        summary="Get a list of event types",
        description="Get a list of event types",
        responses={200: EventTypeSerializer(many=True)},
    )
    # Obtiene los eventos o  tipo de ocasion
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all().order_by('sequence')
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CustomerLifecycleListView(views.APIView):
    model = CustomerLifecycle
    serializer_class = CustomerLifecycleSerializer

    @extend_schema(
        summary="Get a list of customer lifecycles",
        description="Get a list of customer lifecycles",
        responses={200: serializer_class(many=True)},
    )
    # Obtener objetivos del evento en la orden
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class EventGoalListView(views.APIView):
    model = EventGoal
    serializer_class = EventGoalSerializer

    @extend_schema(
        summary="Get a list of event goals",
        description="Get a list of event goals",
        responses={200: serializer_class(many=True)},
    )
    # Obtener mayor información de objetivos filtrado por el customer life cycle
    def get(self, request):
        # filters
        customer_lifecycle = request.GET.get('customer_lifecycle', None)

        paginator = PageNumberPagination()
        instances = self.model.objects.all().order_by('sequence')

        if customer_lifecycle:
            instances = instances.filter(customer_lifecycle__id=customer_lifecycle)

        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MusicAmbianceTypeListView(views.APIView):
    model = MusicAmbianceType
    serializer_class = MusicAmbianceTypeSerializer

    @extend_schema(
        summary="Get a list of music ambiance types",
        description="Get a list of music ambiance types",
        responses={200: serializer_class(many=True)},
    )
    # Obtener el ambiente deseado
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SoundPackageListView(views.APIView):
    model = SoundPackage
    serializer_class = SoundPackageSerializer

    @extend_schema(
        summary="Get a list of sound packages",
        description="Get a list of sound packages",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class OrderServiceTypeListView(views.APIView):
    model = OrderServiceType
    serializer_class = OrderServiceTypeSerializer

    @extend_schema(
        summary="Get a list of order service types",
        description="Get a list of order service types",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# Obtener y cancelar
class OrderOneView(views.APIView):
    permission_classes = [IsAuthenticated]
    model = Order
    serializer_class = OrderListSerializer

    def get(self, request, id):
        instances = self.model.objects.get(order_number=id)
        serializer = self.serializer_class(instances)
        data = serializer.data.copy()
 
        if 'list_musicprojects' in data:
            data['assigs_musicprojects'] = data.pop('list_musicprojects')
        return response.Response(data)

    def put(self, request, id):
        # cancelar una orden
        order_number = id
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        order = self.model.objects.get(order_number=order_number, user_profile=user_profile)
        order.status = "ORDER_CANCELLED"
        order.save()
        serializer = self.serializer_class(order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class OrderTemplateListView(views.APIView):
    model = OrderTemplate
    serializer_class = OrderTemplateSerializer

    @extend_schema(
        summary="Get a list of order templates",
        description="Get a list of order templates",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CountOrdersActiveView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        count = Order.objects.filter(user_profile=user_profile).count()
        return response.Response({"active_orders_count": count}, status=status.HTTP_200_OK)

class ListOrdersActiveView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paginator = PageNumberPagination()
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        instances = Order.objects.filter(user_profile=user_profile).order_by(F('event_date').desc(nulls_last=True), '-id')
        result_page = paginator.paginate_queryset(instances, request)
        serializer = OrderListLevelOneSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ListOrdersByCategoryView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paginator = PageNumberPagination()
        user = request.user.id
        category = request.query_params.get("category")
        user_profile = UserProfile.objects.get(user=user)
        if category:
            instances = Order.objects.filter(user_profile=user_profile, category=category)
        else:
            instances = Order.objects.filter(user_profile=user_profile)
        result_page = paginator.paginate_queryset(instances, request)
        serializer = OrderListLevelOneSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class OrderCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new order",
        description="Create a new order",
        responses={201: OrderSerializer(many=False)},
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            order = serializer.save()

            order_visit_detail = "N/A"
            if order.visit:
                order_visit_detail = f"{order.visit.visit_date.strftime('%Y/%m/%d')} - {order.visit.visit_time.strftime('%H:%M')}"

            equipment_detail = ", ".join(order.additionalequipment_set.values_list("equipment__name", flat=True))
            if not equipment_detail:
                equipment_detail = "N/A"

            # Send email
            """ dynamic_data = {
                "client_name": order.user_profile.user.name,
                "order_number": order.order_number,
                "event_type": order.event_type.name,
                "music_genre_list": ", ".join(order.music_genre_tags.values_list("name", flat=True)),
                "order_service_type": order.service_type.name,
                "order_item": order.item.display_name,
                "specific_services_list": ", ".join(order.orderitem_set.values_list("specific_service__display_name", flat=True).distinct()),
                "extra_equipment": order.get_sound_setup_display(),
                "equipment_list": equipment_detail,
                "visit_date": order_visit_detail,
                "order_date": order.event_date.strftime('%Y/%m/%d'),
                "event_duration": order.get_event_duration_display()
            } """

            """ send_template_email(
                order.user_profile.user.email,
                environ.get("SENDGRID_ORDER_TEMPLATE_ID"),
                dynamic_data
            ) """

            return response.Response({
                "message": "Order created successfully!",
                "order_id": order.order_number
            }, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        paginator = PageNumberPagination()
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        instances = Order.objects.filter(user_profile=user_profile)
        result_page = paginator.paginate_queryset(instances, request)
        serializer = OrderListLevelOneSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class NearestOrderView(views.APIView):
    """
    GET /api/orders/nearest
    Retorna la orden cuya fecha/hora (exec_at) está más cerca de ahora.
    - Considera órdenes futuras y pasadas.
    - Si ambas existen, compara la diferencia absoluta y retorna la más cercana.
    - Si el proyecto requiere limitar por usuario autenticado, se filtra por request.user.
    - Puedes agregar filtros extra (status, etc.) en base a tu negocio.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        qs = Order.objects.all()
        qs = qs.filter(user_profile=user_profile)
        return qs

    def get(self, request):
        now = timezone.localdate()
        qs = self.get_queryset(request)

        future = qs.filter(event_date__gte=now).order_by("event_date").first()
        past = qs.filter(event_date__lt=now).order_by("-event_date").first()

        if not future and not past:
            return response.Response(
                {"detail": "No hay órdenes para evaluar."},
                status=status.HTTP_404_NOT_FOUND,
            )

        candidate = None
        if future and past:
            diff_future = future.event_date - now
            diff_past = now - past.event_date
            candidate = future if diff_future <= diff_past else past
        else:
            candidate = future or past

        data = OrderListSerializer(candidate).data
        return response.Response(data, status=status.HTTP_200_OK)

class OrderItemView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.query_params.get("order")
        paginator = PageNumberPagination()
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        instances = OrderItem.objects.filter(order__order_number=query, order__user_profile=user_profile)
        result_page = paginator.paginate_queryset(instances, request)
        serializer = OrderItemListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class OrderUpdateView(views.APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        order = Order.objects.get(order_number=data.get('order_number'))
        serializer = OrderUpdateSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Exitoso"}, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderAdminView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        instances = Order.objects.all().order_by(F('event_date').desc(nulls_last=True), '-id')
        result_page = paginator.paginate_queryset(instances, request)
        serializer = OrderListLevelOneSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def put(self, request):
        data = request.data.copy()
        order = Order.objects.get(order_number=data.get('order_number'))
        serializer = OrderUpdateOnlyStatusSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Exitoso"}, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MusicProjectsToOrderView(views.APIView):
    permission_classes = [IsAuthenticated]
    model = Order
    serializer_class = OrderListSerializer

    def put(self, request, id):
        user = request.user.id
        user_profile = UserProfile.objects.get(user=user)
        order = self.model.objects.get(order_number=id, user_profile=user_profile)
        music_project_ids = request.data.get("music_project_ids", [])
        order.list_musicprojects.set(music_project_ids)
        order.save()
        serializer = self.serializer_class(order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
