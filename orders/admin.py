from django.contrib import admin
from orders.models import (
    EventType,
    CustomerLifecycle,
    EventGoal,
    MusicAmbianceType,
    OrderServiceType,
    SoundPackage,
    OrderTemplate,
)

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')


@admin.register(CustomerLifecycle)
class CustomerLifecycleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')


@admin.register(EventGoal)
class EventGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')


@admin.register(MusicAmbianceType)
class MusicAmbianceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(OrderServiceType)
class OrderServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')


@admin.register(SoundPackage)
class SoundPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')

@admin.register(OrderTemplate)
class OrderTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
