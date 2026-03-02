from django.contrib import admin
from musicians.models import (
    MusicProject, MusicProjectService, MusicProjectType, TopicArtist, InviteMemberBand,
    CategoryMusic,
)


@admin.register(MusicProjectType)
class MusicProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    list_filter = ('name', 'display_name')


@admin.register(MusicProject)
class MusicProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('project_type', 'created_at')

@admin.register(TopicArtist)
class TopicArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(MusicProjectService)
class MusicProjectServiceAdmin(admin.ModelAdmin):
    list_display = ('music_project', 'is_active')

@admin.register(InviteMemberBand)
class InviteMemberBand(admin.ModelAdmin):
    list_display = ('music_project', 'inviter', 'status')
@admin.register(CategoryMusic)
class CategoryMusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'image')
