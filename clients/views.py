from rest_framework import serializers, views, response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from clients.serializers import ClientTypeSerializer, ClientDetailSerializer, ClientOnboardingDifficultySerializer
from clients.models import ClientType, ClientDetail, ClientOnboardingDifficulty


class ClientTypeListView(views.APIView):
    model = ClientType
    serializer_class = ClientTypeSerializer

    @extend_schema(
        summary="Get a list of client types",
        description="Get a list of client types",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ClientDetailListView(views.APIView):
    model = ClientDetail
    serializer_class = ClientDetailSerializer

    @extend_schema(
        summary="Get a list of client details",
        description="Get a list of client details",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        client_type = request.GET.get('client_type', None)
        paginator = PageNumberPagination()
        instances = self.model.objects.all().order_by('sequence')

        if client_type:
            instances = instances.filter(client_type=client_type)

        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ClientOnboardingDifficultyListView(views.APIView):
    model = ClientOnboardingDifficulty
    serializer_class = ClientOnboardingDifficultySerializer

    @extend_schema(
        summary="Get a list of client difficulties",
        description="Get a list of client difficulties",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):
        role = request.GET.get('role', None)
        paginator = PageNumberPagination()
        instances = self.model.objects.all().order_by('sequence')

        if role:
            instances = instances.filter(role=role)

        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
