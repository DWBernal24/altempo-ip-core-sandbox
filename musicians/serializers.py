import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import check_for_language
from django.views.generic.base import logger
from rest_framework import serializers
from core.serializers import CountrySerializer
from dashboard.serializers import LeanUserSerializer
from musicians.models import (
    AvailabilityInfo,
    AvailabilityInfoDaySchedule,
    AvailabilityInfoTimeSchedule,
    InstrumentSet,
    MusicProjectInstrument,
    MusicProjectInstrumentInstrumentSet,
    MusicProjectService,
    MusicProjectType,
    MusicProject,
    Discography,
    MusicProjectVideo,
    MusicProjectVideoDraft,
    Single,
    MusicProjectImage,
    TopicArtist,
    InviteMemberBand,
    CategoryMusic,
)
from core.models import Instrument, MusicalGenreTag, Language
from services.models import Category, Item, PricingInterval, SpecificService
from services.serializers import (
    CategoryLeanSerializer,
    CategorySerializer,
    ItemLeanSerializer,
    ItemSerializer,
    PricingIntervalSerializer,
    SpecificServiceLeanSerializer,
    SpecificServiceSerializer,
)
from django.db import transaction

from utils.check_urls import check_for_url
from utils.displaySchedule import get_musician_schedule_in_timezone

User = get_user_model()


class CategoryMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMusic
        fields = "__all__"


class ProfileMusicianCoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProject
        fields = ["cover_image"]


class MusicProjectUpdateAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProject
        fields = ["description"]


class ProfileMusicianProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProject
        fields = ["profile_image"]


class TopicArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicArtist
        fields = "__all__"


class ProfileMusicProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProject
        fields = ["project_type"]


class MusicProjectUpdateSerializer(serializers.ModelSerializer):
    music_genre_tags = serializers.PrimaryKeyRelatedField(
        queryset=MusicalGenreTag.objects.all(), many=True, required=False
    )
    languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, required=False
    )

    class Meta:
        model = MusicProject
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "slug"]


class MusicProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProjectType
        fields = "__all__"


class ProfileMusicProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProjectType
        fields = ["id"]


class DiscographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Discography
        fields = ["id", "title", "cover_image", "url_link", "music_project", "type"]
        read_only_fields = ["music_project"]


class BasicCreateMusicProjectSerializer(serializers.Serializer):
    music_project_name = serializers.CharField(required=False)
    music_project_type_id = serializers.IntegerField()
    services = serializers.ListField(child=serializers.IntegerField())


class AlbumSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discography
        fields = ["id", "title"]
        read_only_fields = ["music_project"]


class SingleSerializer(serializers.ModelSerializer):
    album = AlbumSingleSerializer(read_only=True)
    album_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Single
        fields = ["id", "title", "url_link", "music_project", "album", "album_id"]
        read_only_fields = ["music_project"]


class MusicProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProjectImage
        fields = ["id", "image", "caption", "uploaded_at", "thumbnail_position"]
        read_only_fields = ["id", "uploaded_at"]


class InstrumentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name", read_only=True)

    class Meta:
        model = Instrument
        fields = "__all__"


class MusicProjectAddInstrumentsSerializer(serializers.ModelSerializer):
    instrument = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(),
    )
    music_project = serializers.PrimaryKeyRelatedField(
        queryset=MusicProject.objects.all(),
    )
    quantity = serializers.IntegerField(min_value=1)
    brand = serializers.CharField(required=False)
    model = serializers.CharField(required=False)

    class Meta:
        model = MusicProjectInstrument
        fields = ["music_project", "instrument", "quantity", "brand", "model"]


class MusicProjectInstrumentsSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerializer(read_only=True)
    instrument_id = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(), source="instrument", write_only=True
    )
    price_per_instrument = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(required=False)
    model = serializers.CharField(required=False)

    class Meta:
        model = MusicProjectInstrument
        fields = [
            "id",
            "instrument",
            "instrument_id",
            "quantity",
            "music_project",
            "price_per_instrument",
            "brand",
            "model",
        ]
        read_only_fields = ["id", "music_project"]


class InstrumentInSetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    instrument_name = serializers.CharField(
        source="music_project_instrument.instrument.name", read_only=True
    )
    price_per_instrument = serializers.DecimalField(
        source="music_project_instrument.price_per_instrument",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    quantity = serializers.IntegerField(source="quantity_for_set", read_only=True)

    class Meta:
        model = MusicProjectInstrumentInstrumentSet
        fields = ["id", "instrument_name", "price_per_instrument", "quantity"]


class InstrumentInSetQuantitySerializer(serializers.Serializer):
    quantity_for_set = serializers.IntegerField()

    class Meta:
        model = MusicProjectInstrumentInstrumentSet
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.quantity_for_set = validated_data.get("quantity_for_set", instance.quantity_for_set)
        instance.save()
        return instance

class InstrumentSetSerializer(serializers.ModelSerializer):

    instruments = InstrumentInSetSerializer(
        source="musicprojectinstrumentinstrumentset_set", many=True, read_only=True
    )
    music_project = serializers.PrimaryKeyRelatedField(
        queryset=MusicProject.objects.all(),
    )
    calculated_total_price = serializers.SerializerMethodField()

    class Meta:
        model = InstrumentSet
        fields = [
            "id",
            "instrument_set_name",
            "instruments",
            "music_project",
            "calculated_total_price",
        ]
        read_only_fields = ["calculated_total_price", "instruments"]

    def get_calculated_total_price(self, obj):
        if (
            hasattr(obj, "db_calculated_total_price")
            and obj.db_calculated_total_price is not None
        ):
            return obj.db_calculated_total_price
        return obj.calculated_total_price


class AddInstrumentToInstrumentSetSerializer(serializers.Serializer):
    music_project_instrument = serializers.PrimaryKeyRelatedField(
        queryset=MusicProjectInstrument.objects.all(), source="musician_instrument"
    )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class MusicalGenreTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicalGenreTag
        fields = "__all__"


class MusicProjectSerializer(serializers.ModelSerializer):
    instruments = MusicProjectInstrumentsSerializer(
        many=True, read_only=True, source="musicprojectinstrument_set"
    )
    project_type = MusicProjectTypeSerializer(read_only=True)
    music_genre_tags = MusicalGenreTagSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    topics = TopicArtistSerializer(many=True, read_only=True)
    gallery = MusicProjectImageSerializer(many=True, read_only=True)
    country = CountrySerializer(read_only=True)
    service_categories = CategorySerializer(many=True, read_only=True)
    owner = LeanUserSerializer()

    class Meta:
        model = MusicProject
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "slug", "project_type"]


class InviteMemberBandCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteMemberBand
        fields = ["email", "message"]

    def validate_email(self, value):
        music_project = self.context.get("music_project")

        if InviteMemberBand.objects.filter(
            music_project=music_project,
            email=value,
            status=InviteMemberBand.STATUS_INPROCESS,
        ).exists():
            raise serializers.ValidationError(
                "Ya existe una invitación pendiente para este correo."
            )

        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            pass
        else:
            if music_project.owner == user:
                raise serializers.ValidationError("No puedes invitarte a ti mismo.")

        return value

    def create(self, validated_data):
        validated_data["music_project"] = self.context.get("music_project")
        validated_data["inviter"] = self.context.get("request").user
        logger.info(validated_data)

        return super().create(validated_data)


class InviteMemberBandCreateManySerializer(serializers.ModelSerializer):
    # for this serializer, we need to get the list of emails
    emails = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = InviteMemberBand
        fields = ["emails", "message"]

    def validate_emails(self, value):
        """Validate the list of emails"""
        if not value:
            raise serializers.ValidationError("Al menos un email es requerido.")

        music_project = self.context.get("music_project")
        request_user = self.context.get("request").user
        errors = []

        for email in value:
            # Check for pending invitations
            if InviteMemberBand.objects.filter(
                music_project=music_project,
                email=email,
                status=InviteMemberBand.STATUS_INPROCESS,
            ).exists():
                errors.append(f"Ya existe una invitación pendiente para {email}.")
                continue

            # Check if user exists and is the owner
            try:
                user = User.objects.get(email=email)
                if music_project.owner == user:
                    errors.append(f"No puedes invitarte a ti mismo ({email}).")
                    continue
            except User.DoesNotExist:
                pass

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def create(self, validated_data):
        """Create multiple InviteMemberBand instances"""
        emails = validated_data.pop("emails")
        message = validated_data.get("message", "")
        music_project = self.context.get("music_project")
        inviter = self.context.get("request").user

        created_invitations = []

        for email in emails:
            invitation_data = {
                "email": email,
                "message": message,
                "music_project": music_project,
                "inviter": inviter,
                **validated_data,  # Include any other fields
            }

            invitation = InviteMemberBand.objects.create(**invitation_data)
            created_invitations.append(invitation)

        logger.info(f"Created {len(created_invitations)} invitations")

        # Return all created invitations for the view to handle
        return created_invitations


class InviteMemberBandSerializer(serializers.ModelSerializer):
    invited_by_name = serializers.CharField(
        source="invited_by.username", read_only=True
    )
    band_name = serializers.CharField(source="music_project.name", read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = InviteMemberBand
        fields = "__all__"
        read_only_fields = ["id", "status", "created_at", "expires_at", "responded_at"]

class InviteMemberLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteMemberBand
        fields = ["id", "email", "status", "sent_at", "expires_at"]


class MusicProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MusicProjectServiceSerializer(serializers.ModelSerializer):

    # nested serializers for read only operations
    category = CategoryLeanSerializer(read_only=True)
    item = ItemLeanSerializer(read_only=True)
    specific_service = SpecificServiceLeanSerializer(read_only=True)

    # Write fields for POST/PUT requests
    category_id = serializers.CharField(write_only=True)
    service_item_id = serializers.CharField(write_only=True)
    sub_service_id = serializers.CharField(write_only=True)
    pricing_intervals = PricingIntervalSerializer(many=True)
    selected_instruments = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    selected_instrument_set_id = serializers.CharField(
        write_only=True, required=False, allow_null=True
    )
    extra_fields = serializers.DictField(required=False)

    class Meta:
        model = MusicProjectService
        fields = [
            "id",
            "music_project",
            "title",
            "description",
            "is_active",
            "category",
            "item",
            "specific_service",
            # Write-only fields
            "category_id",
            "service_item_id",
            "sub_service_id",
            "selected_instruments",
            "selected_instrument_set_id",
            "extra_fields",
            "pricing_intervals",
            # Read-only nested details
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MusicProjectServiceSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    category = CategoryLeanSerializer(read_only=True)
    item = ItemLeanSerializer(read_only=True)
    specific_service = SpecificServiceLeanSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class MusicProjectServiceCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    music_project_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, default="")
    status = serializers.CharField(default="draft")
    category_id = serializers.CharField()
    service_item_id = serializers.CharField()
    sub_service_id = serializers.CharField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = serializers.CharField(default="USD")
    pricing_intervals = serializers.ListField(child=serializers.DictField())
    attributes = serializers.DictField(default=dict)
    selected_instrument_set_id = serializers.CharField(allow_null=True, required=False)

    def create(self, validated_data):
        # Process the JSON payload and create MusicProjectService
        music_project_id = self.context.get("music_project_id", None)

        if not music_project_id:
            raise serializers.ValidationError("music_project_id is required")

        try:
            music_project = MusicProject.objects.get(id=music_project_id)
        except MusicProject.DoesNotExist:
            raise serializers.ValidationError("MusicProject does not exist")

        category = Category.objects.get(id=validated_data["category_id"])
        service_item = Item.objects.get(name=validated_data["service_item_id"])
        specific_service = SpecificService.objects.get(
            name=validated_data["sub_service_id"]
        )

        # Create the service
        service = MusicProjectService.objects.create(
            music_project=music_project,
            title=validated_data["title"],
            description=validated_data["description"],
            is_active=True if validated_data["status"] == "active" else False,
            category=category,
            item=service_item,
            specific_service=specific_service,
            extra_fields=validated_data["attributes"],
        )

        # relate each interval with the newly created service
        for interval in validated_data["pricing_intervals"]:
            pricing_interval = PricingInterval.objects.create(
                price=interval.get("price"),
                duration=interval.get("duration"),
                unit=interval.get("unit"),
                music_project_service=service,
                is_base=interval.get("is_base", False),
            )

            pricing_interval.save()

        service.save()

        # Set instrument set
        if validated_data.get("selected_instrument_set_id"):
            try:
                instrument_set = InstrumentSet.objects.get(
                    id=validated_data["selected_instrument_set_id"]
                )
                service.selected_instrument_set = instrument_set
                service.save()
            except InstrumentSet.DoesNotExist:
                pass

        return service


class AvailabilityInfoDayScheduleSerializer(serializers.ModelSerializer):
    """Serializer for specific date-based availability"""

    class Meta:
        model = AvailabilityInfoDaySchedule
        fields = ["id", "date", "modality"]

    def validate_date(self, value):
        """Ensure date is not in the past"""
        if value < datetime.datetime.now().date():
            raise serializers.ValidationError("Date cannot be in the past.")
        return value


class AvailabilityInfoTimeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityInfoTimeSchedule
        fields = "__all__"

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"end_time": "End time must be after start time."}
            )

        return data


class AvailabilityInfoUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing availability information"""

    time_schedule_data = AvailabilityInfoTimeScheduleSerializer(
        required=False, many=True
    )
    day_schedule_data = AvailabilityInfoDayScheduleSerializer(required=False, many=True)

    class Meta:
        model = AvailabilityInfo
        fields = ["time_schedule_data", "day_schedule_data"]

    def validate(self, data):
        time_schedule_data = data.get("time_schedule_data")
        day_schedule_data = data.get("day_schedule_data")

        if not time_schedule_data and not day_schedule_data:
            raise serializers.ValidationError(
                "Either time_schedule_data or day_schedule_data must be provided for update."
            )

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        """Update availability info and related schedule"""
        # array with values for a time schedule
        time_schedule_data = validated_data.pop("time_schedule_data", None)
        day_schedule_data = validated_data.pop("day_schedule_data", None)

        if time_schedule_data:
            # delete and repopulate all data with the updated values
            if instance.time_schedule:
                instance.time_schedule.all().delete()

            for sched in time_schedule_data:
                time_schedule = AvailabilityInfoTimeSchedule.objects.create(
                    **sched, availability=instance
                )
                time_schedule.save()

        if day_schedule_data:
            # Remove existing time_schedule if switching to day_schedule
            if instance.day_schedule:
                instance.day_schedule.all().delete()

            for sched in day_schedule_data:
                time_schedule = AvailabilityInfoDaySchedule.objects.create(
                    **sched, availability=instance
                )
                time_schedule.save()

        instance.save()
        return instance


class LeanTimeSchedule(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityInfoTimeSchedule
        fields = ["day", "start_time", "end_time"]


class LeanDaySchedule(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityInfoDaySchedule
        fields = ["date", "modality"]


class AvailabilityInfoSerializer(serializers.ModelSerializer):
    time_schedule = serializers.SerializerMethodField()
    day_schedule = LeanDaySchedule(many=True, read_only=True)

    class Meta:
        model = AvailabilityInfo
        fields = ["id", "time_schedule", "day_schedule"]
        depth = 1

    def get_time_schedule(self, obj):
        """
        Return parsed time schedule according to user's timezone
        """
        request = self.context.get("request")

        # If no request context or no user timezone, return original
        if not request or not hasattr(request.user, "profile"):
            # Return original time_schedule as fallback
            from .serializers import AvailabilityInfoTimeScheduleSerializer

            return AvailabilityInfoTimeScheduleSerializer(
                obj.time_schedule.all(), many=True
            ).data

        customer_timezone = request.user.profile.timezone

        # Get the musician from the availability info
        # Adjust this based on your model relationships
        musician = obj.music_project  # or however you get to the musician

        # Use your helper function
        return get_musician_schedule_in_timezone(
            musician,
            customer_timezone,
        )


class MusicProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProjectVideo
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class MusicProjectVideoDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicProjectVideoDraft
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class MusicProjectVideoDraftCreateSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(required=False, validators=[check_for_url])
    video_url = serializers.URLField()

    class Meta:
        model = MusicProjectVideoDraft
        fields = ["video_url", "caption"]
