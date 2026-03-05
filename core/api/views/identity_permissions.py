from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.models import UserProfile
from core.permissions_matrix import ROLE_PERMISSIONS


class IdentityPermissionsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):

        try:
            profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        role_name = profile.role.name

        permissions = ROLE_PERMISSIONS.get(role_name, [])

        return Response({
            "profile_id": profile.id,
            "role": role_name,
            "permissions": permissions
        })