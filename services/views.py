from rest_framework import serializers, views, response, status
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from services.serializers import (
    TagSerializer,
    CategorySerializer,
    ItemSerializer,
    SpecificServiceSerializer,
    ServiceModeSerializer,
    AttributeSerializer
)
from services.models import Tag, Category, Item, SpecificService, ServiceMode, Attribute


class TagListCreateView(views.APIView):

    @extend_schema(
        summary="Get a list of tags",
        description="Get a list of tags associated with the categories",
        responses={200: TagSerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        tags = Tag.objects.all()
        result_page = paginator.paginate_queryset(tags, request)
        serializer = TagSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    @extend_schema(
        summary="Create a tag",
        description="Create a new tag",
        responses={201: TagSerializer(many=False)},
    )
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailView(views.APIView):
    def get_object(self, pk):
        return Tag.objects.get(pk=pk)

    @extend_schema(
        summary="Get a tag",
        description="Get a specific tag",
        responses={200: TagSerializer(many=False)},
    )
    def get(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return response.Response(serializer.data)

    @extend_schema(
        summary="Update a tag",
        description="Update a specific tag",
        responses={200: TagSerializer(many=False)},
    )
    def put(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a tag",
        description="Delete a specific tag",
    )
    def delete(self, request, pk):
        tag = self.get_object(pk)
        tag.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateView(views.APIView):

    @extend_schema(
        summary="Get all the categories",
        description="Get the list of categories",
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        categories = Category.objects.all()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    @extend_schema(
        summary="Create a category",
        description="Create a new category",
        responses={201: CategorySerializer(many=False)},
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(views.APIView):
    def get_object(self, pk):
        return Category.objects.get(pk=pk)

    @extend_schema(
        summary="Get a category",
        description="Get a category",
        responses={200: CategorySerializer(many=False)},
    )
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return response.Response(serializer.data)

    @extend_schema(
        summary="Update a categoty",
        description="Update a category",
        responses={200: CategorySerializer(many=False)},
    )
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a categoty",
        description="Delete a category"
    )
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ItemListCreateView(views.APIView):

    @extend_schema(
        summary="Get all the items",
        description="Get the list of items",
        responses={200: ItemSerializer(many=True)},
    )
    def get(self, request):
        # Get filters
        category = request.GET.get('category', None)
        paginator = PageNumberPagination()
        items = Item.objects.all()

        if category:
            items = items.filter(category__id=category)

        result_page = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create one item",
        description="Create one item",
        responses={201: ItemSerializer(many=False)},
    )
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(views.APIView):

    @extend_schema(
        summary="Create an item",
        description="Create an item",
        responses={200: ItemSerializer(many=False)},
    )
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return response.Response(serializer.data)

    @extend_schema(
        summary="Update an item",
        description="Update an item",
        responses={200: ItemSerializer(many=False)},
    )
    def put(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete an item",
        description="Delete an item",
    )
    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SpecificServiceListCreateView(views.APIView):

    @extend_schema(
        summary="Get all the specific services",
        description="Get the list of specific services",
        responses={200: SpecificServiceSerializer(many=True)},
    )
    def get(self, request):
        item = request.GET.get('item', None)
        paginator = PageNumberPagination()
        services = SpecificService.objects.all()
        if item:
            services = services.filter(item=item)

        result_page = paginator.paginate_queryset(services, request)
        serializer = SpecificServiceSerializer(result_page, many=True)
        return  paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create a specific services",
        description="Create a specific services",
        responses={201: SpecificServiceSerializer(many=False)},
    )
    def post(self, request):
        serializer = SpecificServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificServiceDetailView(views.APIView):

    @extend_schema(
        summary="Get a specific services",
        description="Get a specific services",
        responses={200: SpecificServiceSerializer(many=False)},
    )
    def get(self, request, pk):
        service = SpecificService.objects.get(pk=pk)
        serializer = SpecificServiceSerializer(service)
        return response.Response(serializer.data)

    @extend_schema(
        summary="Update a specific services",
        description="Update a specific services",
        responses={200: SpecificServiceSerializer(many=False)},
    )
    def put(self, request, pk):
        service = SpecificService.objects.get(pk=pk)
        serializer = SpecificServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="Delete a specific services",
        description="Delete a specific services"
    )
    def delete(self, request, pk):
        service = SpecificService.objects.get(pk=pk)
        service.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ServiceModeListCreateView(views.APIView):

    @extend_schema(
        summary="Get all the service modes",
        description="List of service modes",
        responses={200: ServiceModeSerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        service_modes = ServiceMode.objects.all()
        result_page = paginator.paginate_queryset(service_modes, request)
        serializer = ServiceModeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create a service mode",
        description="Create a service mode",
        responses={201: ServiceModeSerializer(many=False)},
    )
    def post(self, request):
        serializer = ServiceModeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceModeDetailView(views.APIView):

    @extend_schema(
        summary="Get a service mode",
        description="Get a service mode",
        responses={200: ServiceModeSerializer(many=False)},
    )
    def get(self, request, pk):
        service_mode = ServiceMode.objects.get(pk=pk)
        serializer = ServiceModeSerializer(service_mode)
        return response.Response(serializer.data)

    @extend_schema(
        summary="Update a service mode",
        description="Update a service mode",
        responses={200: ServiceModeSerializer(many=False)},
    )
    def put(self, request, pk):
        service_mode = ServiceMode.objects.get(pk=pk)
        serializer = ServiceModeSerializer(service_mode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a service mode",
        description="Delete a service mode",
    )
    def delete(self, request, pk):
        service = ServiceMode.objects.get(pk=pk)
        service.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class AttributeListCreateView(views.APIView):

    @extend_schema(
        summary="List of attributes",
        description="List of attributes",
        responses={200: AttributeSerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        attribute = Attribute.objects.all()
        result_page = paginator.paginate_queryset(attribute, request)
        serializer = AttributeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create attribute",
        description="Create attribute",
        responses={201: AttributeSerializer(many=False)},
    )
    def post(self, request):
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttributeDetailView(views.APIView):

    @extend_schema(
        summary="Get a attribute",
        description="Get a attribute",
        responses={200: AttributeSerializer(many=False)},
    )
    def get(self, request, pk):
        attribute = Attribute.objects.get(pk=pk)
        serializer = AttributeSerializer(attribute)
        return response.Response(serializer.data)

    @extend_schema(
        summary="Update a attribute",
        description="Update a attribute",
        responses={200: AttributeSerializer(many=False)},
    )
    def put(self, request, pk):
        attribute = Attribute.objects.get(pk=pk)
        serializer = AttributeSerializer(attribute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a attribute",
        description="Delete a attribute"
    )
    def delete(self, request, pk):
        attribute = Attribute.objects.get(pk=pk)
        attribute.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
