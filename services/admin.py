from django.contrib import admin
from services.models import Tag, Category, Item, SpecificService, ServiceMode, Attribute


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','display_name')


@admin.register(SpecificService)
class SpecificServiceAdmin(admin.ModelAdmin):
    list_display = ('name','display_name')


@admin.register(ServiceMode)
class ServiceModeAdmin(admin.ModelAdmin):
    list_display = ('name','display_name')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name','display_name')
