from django.contrib import admin
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
    Equipment
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code')


@admin.register(ReferralSource)
class ReferralSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MusicalGenreTag)
class MusicalGenreTagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MusicianVoiceType)
class MusicianVoiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(VocalStyle)
class VocalStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(DJType)
class DJTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(CollabType)
class CollabTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Equipment)
class CollabTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'inventory')


