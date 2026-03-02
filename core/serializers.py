from rest_framework import serializers

from core.models import CollabType
from core.models import Country
from core.models import DJType
from core.models import Equipment
from core.models import Gender
from core.models import Instrument
from core.models import Language
from core.models import MusicalGenreTag
from core.models import MusicianVoiceType
from core.models import Notification
from core.models import ReferralSource
from core.models import VocalStyle
from musicians.models import InviteMemberBand


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ReferralSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralSource
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class MusicalGenreTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicalGenreTag
        fields = "__all__"


class MusicianVoiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicianVoiceType
        fields = "__all__"


class VocalStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocalStyle
        fields = "__all__"


class InstrumentSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="type.display_name")
    category_display = serializers.CharField(source="category.display_name")

    class Meta:
        model = Instrument
        fields = "__all__"


class DJTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJType
        fields = "__all__"


class CollabTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollabType
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "type",
            "user",
            "created_at",
            "read",
            "redirect_link",
            "values",
            "detail",
            "title",  # deprecated, kept for backward compatibility
            "message",  # deprecated, kept for backward compatibility
        ]
        read_only_fields = ["id", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Handle INVITE_BAND_MEMBER special case
        # Add invitation status to values for frontend use
        if instance.type == Notification.INVITE_BAND_MEMBER and instance.values:
            try:
                invitation_id = instance.values.get("invitation_id")
                if invitation_id:
                    invitation = InviteMemberBand.objects.get(id=invitation_id)
                    # Add invitation status to the response
                    data["invitation_status"] = invitation.status

                    # Ensure values contains the status (in case backend didn't set it)
                    if data.get("values"):
                        data["values"]["invitation_status"] = invitation.status

            except (InviteMemberBand.DoesNotExist, ValueError, TypeError):
                pass

        return data
