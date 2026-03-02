from os import environ
from rest_framework import serializers, views, response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from roles.serializers import (
    RoleSerializer, UserProfileSerializer, UserProfileGetSerializer, DemografySerializer, KeyDatesSerializer,
    ListDeListDemografyProfileSerializer, KeyDatesProfileSerializer, ListDeListDemografyProfileExtraSerializer,
    KeyDatesProfileExtraSerializer,
)
from roles.models import Role, UserProfile, Demografy, KeyDates, ListDemografyProfile, KeyDatesProfile
from utils.email import send_template_email


class RoleListCreateView(views.APIView):

    @extend_schema(
        summary="Get the list of roles",
        description="Get the list of roles",
        responses={200: RoleSerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        roles = Role.objects.all()
        result_page = paginator.paginate_queryset(roles, request)
        serializer = RoleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create a role",
        description="Create a role",
        responses={201: RoleSerializer(many=False)},
    )
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DemografyView(views.APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        demografies = Demografy.objects.all()
        result_page = paginator.paginate_queryset(demografies, request)
        serializer = DemografySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class KeyDatesView(views.APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        data = KeyDates.objects.all()
        result_page = paginator.paginate_queryset(data, request)
        serializer = KeyDatesSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ListDeListDemografyProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paginator = PageNumberPagination()
        user = request.user
        profile = UserProfile.objects.get(user=user)
        data = ListDemografyProfile.objects.filter(profile=profile)
        result_page = paginator.paginate_queryset(data, request)
        serializer = ListDeListDemografyProfileExtraSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        data = request.data.copy()
        data['profile'] = profile.id
        serializer = ListDeListDemografyProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.query_params.get("id")
        if not pk:
             return response.Response({"message": "Parametro no definido"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        profile = UserProfile.objects.get(user=user)
        ListDemografyProfile.objects.filter(id=pk, profile=profile).delete()
        return response.Response({"message": "Parametro no definido"}, status=status.HTTP_200_OK)

class KeyDatesProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paginator = PageNumberPagination()
        user = request.user
        profile = UserProfile.objects.get(user=user)
        data = KeyDatesProfile.objects.filter(profile=profile)
        result_page = paginator.paginate_queryset(data, request)
        serializer = KeyDatesProfileExtraSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        data = request.data.copy()
        data['profile'] = profile.id
        serializer = KeyDatesProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.query_params.get("id")
        if not pk:
             return response.Response({"message": "Parametro no definido"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        profile = UserProfile.objects.get(user=user)
        KeyDatesProfile.objects.filter(id=pk, profile=profile).delete()
        return response.Response({"message": "Parametro no definido"}, status=status.HTTP_200_OK)

class UserProfileCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create user profile",
        description="Create user profile with basic information",
        responses={201: UserProfileSerializer(many=False)},
    )
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        data['name'] = request.user.name

        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Send new user email
            send_template_email(
                request.user.email,
                environ.get("SENDGRID_NEW_USER_TEMPLATE_ID"),
                {
                    "name":  request.user.name,
                    "login_url": environ.get("LOGIN_URL")
                },
                False
            )

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileGetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return response.Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileGetSerializer(profile)

        return response.Response(serializer.data)
