from datetime import datetime
from zoneinfo import ZoneInfo
from rest_framework import generics, serializers, views, response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from core.models import (
    Country,
    ReferralSource,
    Gender,
    MusicalGenreTag,
    MusicianVoiceType,
    VocalStyle,
    Instrument,
    DJType,
    CollabType,
    Equipment,
    Language,
    Notification,
)
from core.serializers import (
    CountrySerializer,
    ReferralSourceSerializer,
    GenderSerializer,
    MusicalGenreTagSerializer,
    MusicianVoiceTypeSerializer,
    VocalStyleSerializer,
    InstrumentSerializer,
    DJTypeSerializer,
    CollabTypeSerializer,
    EquipmentSerializer,
    LanguageSerializer,
    NotificationSerializer,
)


class CountryListView(views.APIView):
    model = Country
    serializer_class = CountrySerializer

    @extend_schema(
        summary="Get a list of contries",
        description="Get a list of contries",
        responses={200: CountrySerializer(many=True)},
    )
    def get(self, request):
        instances = self.model.objects.all()
        serializer = self.serializer_class(instances, many=True)
        return response.Response(serializer.data)


class ReferralSourceListView(views.APIView):
    model = ReferralSource
    serializer_class = ReferralSourceSerializer

    @extend_schema(
        summary="Get a list of referral sources",
        description="Get a list of referral sources",
        responses={200: ReferralSourceSerializer(many=True)},
    )
    def get(self, request):
        instances = self.model.objects.all()
        serializer = self.serializer_class(instances, many=True)
        return response.Response(serializer.data)


class GenderListView(views.APIView):
    model = Gender
    serializer_class = GenderSerializer

    @extend_schema(
        summary="Get a list of genders",
        description="Get a list of genders",
        responses={200: GenderSerializer(many=True)},
    )
    def get(self, request):
        instances = self.model.objects.all().order_by("sequence")
        serializer = self.serializer_class(instances, many=True)
        return response.Response(serializer.data)


class MusicalGenreTagListView(views.APIView):
    model = MusicalGenreTag
    serializer_class = MusicalGenreTagSerializer

    @extend_schema(
        summary="Get a list of musical genre tags",
        description="Get a list of musical genre tags",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class LanguagesListView(views.APIView):
    model = Language
    serializer_class = LanguageSerializer

    @extend_schema(
        summary="Get a list of languages",
        description="Get a list of languages",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MusicianVoiceTypeListView(views.APIView):
    model = MusicianVoiceType
    serializer_class = MusicianVoiceTypeSerializer

    @extend_schema(
        summary="Get a list of musician voice types",
        description="Get a list of musician voice types",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class VocalStyleListView(views.APIView):
    model = VocalStyle
    serializer_class = VocalStyleSerializer

    @extend_schema(
        summary="Get a list of vocal styles",
        description="Get a list of vocal styles",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class InstrumentListView(generics.ListAPIView):
    serializer_class = InstrumentSerializer
    pagination_class = None

    def get_queryset(self):

        instruments = cache.get("instrument_list")
        if not instruments:
            instruments = list(
                Instrument.objects.select_related("type", "category").all()
            )
            cache.set("instrument_list", instruments, 3600)

        return Instrument.objects.select_related("type", "category").all()


class DJTypeListView(views.APIView):
    model = DJType
    serializer_class = DJTypeSerializer

    @extend_schema(
        summary="Get a list of DJ types",
        description="Get a list of DJ types",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CollabTypeListView(views.APIView):
    model = CollabType
    serializer_class = CollabTypeSerializer

    @extend_schema(
        summary="Get a list of collab types",
        description="Get a list of collab types",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class EquipmentListView(views.APIView):
    model = Equipment
    serializer_class = EquipmentSerializer

    @extend_schema(
        summary="Get a list of equipment",
        description="Get a list of equipment",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class NotificationView(views.APIView):
    model = Notification
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get a list of notifications",
        description="Get a list of notifications",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()

        last_event_id = request.query_params.get("last_event_id")
        notification_type = request.query_params.get("notification_type")
        user_notifications = request.user.user_notification

        if last_event_id:
            user_notifications = user_notifications.filter(id__gt=last_event_id)

        if notification_type:
            user_notifications = user_notifications.filter(type=notification_type)

        user_notifications = user_notifications.order_by("-id")

        result_page = paginator.paginate_queryset(user_notifications, request)
        serializer = self.serializer_class(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def patch(self, request, pk):
        notification = Notification.objects.get(id=pk)

        notification.read = True
        notification.save()

        return response.Response({"success": True})


class TimeZoneView(views.APIView):

    def get(self, request):
        common_timezones = [
            "UTC",
            "America/New_York",
            "America/Chicago",
            "America/Denver",
            "America/Los_Angeles",
            "America/Anchorage",
            "Pacific/Honolulu",
            "America/Mexico_City",
            "America/Toronto",
            "America/Vancouver",
            "America/El_Salvador",
            "America/Sao_Paulo",
            "America/Argentina/Buenos_Aires",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Europe/Madrid",
            "Europe/Rome",
            "Europe/Moscow",
            "Africa/Cairo",
            "Africa/Johannesburg",
            "Asia/Dubai",
            "Asia/Kolkata",
            "Asia/Shanghai",
            "Asia/Tokyo",
            "Asia/Seoul",
            "Asia/Singapore",
            "Asia/Hong_Kong",
            "Australia/Sydney",
            "Australia/Melbourne",
            "Pacific/Auckland",
        ]

        timezone_data = []
        now = datetime.now()

        for tz_name in common_timezones:
            try:
                tz = ZoneInfo(tz_name)
                dt = now.astimezone(tz)

                timezone_data.append(
                    {
                        "value": tz_name,
                        "label": tz_name.replace("_", " "),
                        "offset": dt.strftime("%z"),
                        "display": f"{tz_name.replace('_', ' ')} (UTC{dt.strftime('%z')})",
                    }
                )
            except Exception:
                continue

        return response.Response(
            {"count": len(timezone_data), "timezones": timezone_data}
        )
